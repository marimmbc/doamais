describe('Adicionar item para doação', () => {
    it('deve acessar a página de início, realizar o login e adicionar um item para doação', () => {
        // Acessa a página inicial
        cy.visit('http://127.0.0.1:8000/');  // Altere o URL conforme necessário

        // Clica no botão de login
        cy.get('button').contains('Entrar').click();

        // Preenche as informações de login e submete o formulário
        cy.get('input[id="username"]').type('mmbc');
        cy.get('input[id="password"]').type('mari1402');
        cy.get('form.login-form').submit();

        // Acessa a página de pesquisar após o login
        cy.visit('http://127.0.0.1:8000/pesquisar');  // Altere o URL conforme necessário

        // Preenche o formulário de pesquisa
        cy.get('input[id="title"]').type('primeiro teste');
        cy.get('select[id="category"]').select('clothes');
        cy.get('select[id="condition"]').select('new');

        // Submete o formulário de pesquisa
        cy.get('button').contains('Pesquisar').click();

        // Confirmação do teste e verificação da página de resultados
        cy.url().should('include', '/pesquisar');
        cy.contains('Nome: primeiro teste').should('exist');
    });
});
