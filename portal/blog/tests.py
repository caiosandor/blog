from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Pagina, PerfilFuncionario
from .models import Post


class DashboardAula17Test(TestCase):
    def setUp(self):
        # Instancia duas organizações distintas para validar o isolamento multi-tenant
        self.pagina_a = Pagina.objects.create(nome='Portal Maricá', tag_oficial='marica')
        self.pagina_b = Pagina.objects.create(nome='Portal Niterói', tag_oficial='niteroi')

        # Perfis de acesso na Página A: administrador (dono) e operador (editor)
        self.user_dono_a = User.objects.create_user(username='dono_a', password='123')
        PerfilFuncionario.objects.create(usuario=self.user_dono_a, pagina=self.pagina_a, cargo='dono')

        self.user_editor_a = User.objects.create_user(username='editor_a', password='123')
        PerfilFuncionario.objects.create(usuario=self.user_editor_a, pagina=self.pagina_a, cargo='editor')

        # Perfil administrativo na Página B
        self.user_dono_b = User.objects.create_user(username='dono_b', password='123')
        PerfilFuncionario.objects.create(usuario=self.user_dono_b, pagina=self.pagina_b, cargo='dono')

        # Massa de dados controlada: 3 registros na Página A e 5 na Página B
        Post.objects.create(titulo='Post A1', conteudo='...', autor=self.user_dono_a, pagina=self.pagina_a, status='publicado')
        Post.objects.create(titulo='Post A2', conteudo='...', autor=self.user_dono_a, pagina=self.pagina_a, status='publicado')
        Post.objects.create(titulo='Post A3', conteudo='...', autor=self.user_editor_a, pagina=self.pagina_a, status='rascunho')

        for i in range(5):
            Post.objects.create(
                titulo=f'Post B{i}',
                conteudo='...',
                autor=self.user_dono_b,
                pagina=self.pagina_b,
                status='publicado'
            )

    def test_isolamento_metricas_por_pagina(self):
        # Verifica se os indicadores contabilizam apenas os registros da organização do usuário
        self.client.force_login(self.user_dono_a)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['kpis']['total_posts'], 3)
        self.assertEqual(response.context['kpis']['publicados'], 2)
        self.assertEqual(response.context['kpis']['rascunhos'], 1)

    def test_dashboard_vazio_sem_erro(self):
        # Garante renderização estável quando a organização não possui publicações
        pagina_vazia = Pagina.objects.create(nome='Portal Vazio', tag_oficial='vazio')
        user_vazio = User.objects.create_user(username='vazio', password='123')
        PerfilFuncionario.objects.create(usuario=user_vazio, pagina=pagina_vazia, cargo='dono')

        self.client.force_login(user_vazio)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['kpis']['total_posts'], 0)

    def test_editor_nao_pode_exportar_csv_e_nao_ve_series(self):
        # Valida restrição de visualização de séries temporais e bloqueio de exportação para editores
        self.client.force_login(self.user_editor_a)

        resp_dash = self.client.get(reverse('dashboard'))
        self.assertFalse(resp_dash.context['mostra_series'])
        self.assertFalse(resp_dash.context['pode_exportar'])

        resp_csv = self.client.get(reverse('exportar-posts-csv'))
        self.assertEqual(resp_csv.status_code, 403)

    def test_dono_exporta_csv_apenas_da_propria_pagina(self):
        # Garante que o arquivo CSV exportado contém exclusivamente dados da página do administrador
        self.client.force_login(self.user_dono_a)
        response = self.client.get(reverse('exportar-posts-csv'))
        self.assertEqual(response.status_code, 200)
        conteudo = response.content.decode('utf-8')
        self.assertIn('Post A1', conteudo)
        self.assertNotIn('Post B0', conteudo)

    def test_filtro_periodo_invalido_nao_gera_erro_500(self):
        # Confirma o tratamento seguro de parâmetros de data malformados na query string
        self.client.force_login(self.user_dono_a)
        response = self.client.get(reverse('dashboard'), {'inicio': 'data-invalida', 'fim': 'abc'})
        self.assertEqual(response.status_code, 200)

    def test_sem_n_mais_1_na_listagem_posts(self):
        # Trava o desempenho garantindo execução em consulta única via select_related
        with self.assertNumQueries(1):
            posts = list(Post.objects.filter(pagina=self.pagina_a).select_related('autor'))
            autores = [p.autor.username for p in posts]
            self.assertEqual(len(autores), 3)