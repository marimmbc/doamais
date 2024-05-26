describe('Doação de Item', () => {
    it('Adiciona um item para doação', () => {
        // Acessar a página de início
        cy.visit('http://localhost:8000/inicio');

        // Clicar no botão de Login
        cy.get('.welcome-container button').contains('Entrar').click();

        // Preencher as informações de login e submeter o formulário
        cy.get('#username').type('mmbc');
        cy.get('#password').type('mari1402');
        cy.get('.login-form').submit();

        // Supõe-se que o usuário será redirecionado para a página de pesquisa após o login
        // Preencher o formulário de pesquisa
        cy.get('#title').type('primeiro teste');
        cy.get('#category').select('clothes');
        cy.get('#condition').select('new');

        // Submeter o formulário de pesquisa
        cy.get('form').contains('Pesquisar').click();

        // Adicionar verificações para confirmar que a página de resultados foi carregada ou que o item foi adicionado
        // Exemplo: verificar se existe algum item nos resultados da pesquisa
        cy.get('.search-results').should('contain', 'primeiro teste');
    });
});
