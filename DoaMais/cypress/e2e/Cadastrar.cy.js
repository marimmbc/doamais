describe('Cadastro e Redirecionamento para Pesquisar', () => {
  it('visita a página inicial e cadastra um novo usuário', () => {
      // Visit the Inicio page
      cy.visit('/');

      // Click on the "Cadastrar" button
      cy.contains('button', 'Cadastrar').click();

      // Ensure the page has redirected to the "Cadastro" page
      cy.url().should('include', '/cadastrar');

      // Fill the registration form
      cy.get('input[name="username"]').type('g0j0u');
      cy.get('input[name="email"]').type('gojosatoru@jjk.com');
      cy.get('input[name="password1"]').type('jujutsu');
      cy.get('input[name="password2"]').type('jujutsu');

      const filePath = 'gojo_icon.jpg';
      cy.get('input[type="file"]').attatchFile(filePath); 

      // Click on the "Cadastrar" button to submit the form
      cy.get('button[type="submit"]').contains('Cadastrar').click();

      // Check if the user is redirected to the "Pesquisar" page after registration
      cy.url({ timeout: 10000 }).should('include', '/pesquisar');
  });
});
