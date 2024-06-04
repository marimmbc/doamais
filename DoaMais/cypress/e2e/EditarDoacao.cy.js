describe('Teste de edição de item de doação', () => {
  it('Deve permitir ao usuário editar um item de doação', () => {
    cy.visit('http://127.0.0.1:8000/'); // Substitua pela URL correta
    cy.get('button').contains('Entrar').click();

    cy.get('input#username').type('mmbc');
    cy.get('input#password').type('mari1402');
    cy.get('button').contains('Entrar').click();

    cy.url().should('include', '/pesquisar');
    cy.get('a').contains('Minhas Doações').click();

    cy.url().should('include', '/minhas_doacoes');
    cy.get('a').contains('Carro de Brinquedo').click();

    cy.url().should('include', '/descricao_minhas_doacoes');
    cy.get('a').contains('Editar').click().then(() => {
      cy.log('Botão Editar clicado');
    });

    cy.url({ timeout: 10000 }).should('include', '/editar_doacao').then(() => {
      cy.log('Página de edição carregada');
    });

    cy.get('select#condition').select('used_good');
    cy.get('button').contains('Salvar').click();

    cy.url().should('include', '/minhas_doacoes').then(() => {
      cy.log('Edição bem-sucedida');
    });
  });
});
