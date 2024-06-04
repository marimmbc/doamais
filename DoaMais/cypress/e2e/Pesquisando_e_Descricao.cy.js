describe('Teste de solicitação de item', () => {
    it('Deve permitir ao usuário solicitar um item', () => {
      // Visitar a página inicial e clicar em "Entrar"
      cy.visit('http://127.0.0.1:8000/'); // Substitua pela URL correta
      cy.get('button').contains('Entrar').click();
  
      // Preencher o formulário de login e submeter
      cy.get('input#username').type('g0j0u');
      cy.get('input#password').type('jujutsu');
      cy.get('button').contains('Entrar').click();
  
      // Esperar que a página de pesquisa carregue
      cy.url().should('include', '/pesquisar');
  
      // Preencher o formulário de pesquisa
      cy.get('input#title').type('Carro de Brinquedo');
      cy.get('select#category').select('toy');
      cy.get('select#condition').select('used_good');
      cy.get('button#search').click();
  
      // Esperar que o resultado da pesquisa apareça e clicar na imagem do item
      cy.wait(5000); // Espera 5 segundos
      cy.get('.search-item img').first().click(); // Assume que a primeira imagem é a do item procurado
  
      // Esperar que a página de descrição do item carregue e clicar em "Solicitar Item"
      cy.url().should('include', '/descricao_item');
      cy.wait(5000); // Espera 5 segundos
      cy.get('form button').contains('Solicitar Item').click();
    });
  });
  