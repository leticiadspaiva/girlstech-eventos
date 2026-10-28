# 🌸 Girls Tech - Calendário de Eventos de Tecnologia (2026/2027)

Bem-vindo(a) ao repositório do **Girls Tech**, uma Single Page Application (SPA) pública e automatizada, desenvolvida para mapear e organizar os principais eventos de tecnologia, universidades e multinacionais acontecendo em todos os estados do Brasil e em formato 100% online.

## 🎯 O Projeto
A plataforma visa democratizar e facilitar o acesso à informação sobre eventos tecnológicos (gratuitos e pagos, incluindo conferências de Big Techs, encontros de comunidades e eventos de LinkedIn). A ferramenta centraliza tudo em uma interface interativa, focada na usabilidade, garantindo que o conhecimento e as oportunidades de networking cheguem a mais mulheres, independentemente da sua região.

## 🚀 Funcionalidades
- **Acesso Público e Gratuito:** Plataforma aberta para toda a comunidade (sem barreiras de login).
- **Destaque 100% Online:** Área exclusiva no topo do site para eventos virtuais sem fronteiras.
- **Navegação Geográfica:** Eventos presenciais categorizados por Região (Norte, Nordeste, Centro-Oeste, Sudeste e Sul) e Estado.
- **Ordenação Inteligente:** O sistema organiza automaticamente os eventos de forma cronológica (do mais antigo para o mais recente) e sinaliza visualmente se o evento está "Em breve" ou "Concluído" com base na data atual.
- **Arquitetura Desacoplada (CMS):** A interface visual (HTML/JS) é separada do banco de dados (JSON), permitindo atualizações de conteúdo sem risco de quebra de layout.
- **Integração e Entrega Contínuas (CI/CD):** Automação via GitHub Actions que atua como um "fiscal de qualidade", validando a estrutura dos dados inseridos antes de atualizar o site no ar.

## 🛠️ Tecnologias Utilizadas
- **HTML5 & CSS3 (Tailwind CSS):** Estruturação semântica e estilização responsiva ágil.
- **JavaScript (Vanilla) & Fetch API:** Lógica de manipulação do DOM e consumo assíncrono dos dados.
- **JSON:** Banco de dados estático e leve (`eventos.json`).
- **GitHub Pages:** Hospedagem gratuita e contínua do site estático.
- **GitHub Actions:** Automação de validação de código (CI).

## 🎨 UI/UX e Paleta de Cores
O design foi construído em torno da identidade visual oficial da comunidade Girls Tech:
- **Primary:** `#D84272` (Rosa Escuro/Magenta) - Botões e Destaques
- **Secondary:** `#FDBFD6` (Rosa Claro) - Elementos de apoio
- **Cream:** `#FFF1E8` (Fundo Principal) - Leitura confortável
- **Dark:** `#953352` (Textos e Títulos) - Contraste e acessibilidade
- **Soft:** `#F4F2E5` (Fundo de Cartões)

---

## 📝 Como Cadastrar Novos Eventos (Guia para o Comitê)

A plataforma foi construída para que **qualquer pessoa**, mesmo sem conhecimento de programação, possa adicionar novos eventos de forma segura. Todos os dados ficam centralizados no arquivo `eventos.json`.

### Passo a Passo da Inclusão:
1. Acesse este repositório no GitHub.
2. Clique no arquivo chamado `eventos.json`.
3. No canto superior direito da caixa de código, clique no **ícone de Lápis (Edit this file)**.
4. Identifique o bloco do Estado desejado (ex: `"SP": [`) ou a seção `"ONLINE": [`.
5. Copie a estrutura de um evento existente e cole na linha abaixo (lembre-se de separar cada evento com uma vírgula `,`).
6. Altere as informações entre as aspas duplas `""`.
7. Clique no botão verde **Commit changes...** para salvar.

### Entendendo a Estrutura de um Evento
Cada evento obedece à seguinte estrutura:
```json
{ 
  "title": "Nome do Evento", 
  "category": "GRANDE EVENTO", 
  "cost": "Gratuito", 
  "date": "2026-11-20", 
  "displayDate": "20 de Novembro, 2026", 
  "link": "[https://link-de-inscricao.com](https://link-de-inscricao.com)" 
}
