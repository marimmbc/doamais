describe('Teste de adicionar item para doação', () => {
  it('Deve permitir ao usuário adicionar um novo item para doação', () => {
    // Visitar a página inicial e clicar em "Entrar"
    cy.visit('http://127.0.0.1:8000/'); // Substitua pela URL correta
    cy.get('button').contains('Entrar').click();

    // Preencher o formulário de login e submeter
    cy.get('input#username').type('mmbc');
    cy.get('input#password').type('mari1402');
    cy.get('button').contains('Entrar').click();

    // Esperar que a página de pesquisa carregue e navegar para "Minhas Doações"
    cy.url({ timeout: 10000 }).should('include', '/pesquisar');
    cy.get('a').contains('Minhas Doações').click();

    // Na página de "Minhas Doações", clicar no botão para doar novo item
    cy.url().should('include', '/minhas_doacoes');
    cy.get('button').contains('Fazer Nova Doação').click(); // Assegure-se que este botão está corretamente identificado no HTML

    // Preencher o formulário de doação de item
    cy.url().should('include', '/doar_item');
    
    cy.get('input[type="file"]').attachFile( 'carro_vermelho.jpeg'); 

    // Preencher os campos do formulário
    cy.get('input#item_name').type('Carro de Brinquedo');
    cy.get('select#category').select('toy');
    cy.get('select#condition').select('new');
    cy.get('input#location').type('Recife, PE');
    cy.get('textarea#description').type('Carro de brinquedo pequeno e vermelho');

    // Submeter o formulário
    cy.get('button#submit').click();

  });
});
