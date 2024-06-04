describe('Teste de favoritar item', () => {
    it('Deve permitir ao usuário favoritar um item e verificar nos favoritos', () => {
      // Visitar a página inicial e clicar em "Entrar"
      cy.visit('http://127.0.0.1:8000/'); // Substitua pela URL correta
      cy.get('button').contains('Entrar').click();
  
      // Preencher o formulário de login e submeter
      cy.get('input#username').type('g0j0u');
      cy.get('input#password').type('jujutsu');
      cy.get('button').contains('Entrar').click();
  
      // Selecionar a opção 'Móveis' na navbar
      cy.get('li.dropdown').contains('Categorias').click();
      cy.get('li.dropdown ul.dropdown-menu li').contains('Móveis').click();
  
      // Esperar que os resultados apareçam
      cy.wait(5000); // Espera 5 segundos
  
      // Selecionar a estrela para favoritar o item 'Sofá Vermelho'
      cy.get('.search-item').contains('Sofá Vermelho').parent().find('.star').click();
  
      // Esperar 5 segundos
      cy.wait(5000); // Espera 5 segundos
  
      // Selecionar a aba de 'Favoritos' na navbar
      cy.get('li').contains('Favoritos').click();
  
      // Esperar que os resultados de favoritos apareçam
      cy.wait(5000); // Espera 5 segundos
    });
  });
  