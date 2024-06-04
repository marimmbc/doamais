describe('Teste de avaliação de item solicitado', () => {
  it('Deve permitir ao usuário avaliar um item solicitado', () => {
      // Visitar a página inicial e clicar em "Entrar"
      cy.visit('http://127.0.0.1:8000/'); // Substitua pela URL correta
      cy.get('button').contains('Entrar').click();

      // Preencher o formulário de login e submeter
      cy.get('input#username').type('g0j0u');
      cy.get('input#password').type('jujutsu');
      cy.get('button').contains('Entrar').click();

      // Selecionar a opção 'Itens Solicitados' na navbar
      cy.get('a').contains('Meus itens Solicitados').click();

      // Esperar 5 segundos para a página carregar
      cy.wait(5000);

      // Clicar no botão 'Avaliar' para o item 'Carro de Brinquedo'
      cy.get('tr').contains('Carro de Brinquedo').parent().find('a').contains('Avaliar').click();

      // Na página de avaliação, simular a interação do usuário para tornar os inputs visíveis
      cy.get('label[for="disponibilidade_4"]').click();
      cy.get('label[for="condicao_3"]').click();
      cy.get('label[for="higiene_5"]').click();
      cy.get('label[for="adequacao_4"]').click();

      // Selecionar as estrelas e preencher a observação
      cy.get('input#disponibilidade_4').check({ force: true });
      cy.get('input#condicao_3').check({ force: true });
      cy.get('input#higiene_5').check({ force: true });
      cy.get('input#adequacao_4').check({ force: true });
      cy.get('textarea#observacao').type('O recebimento do item foi fácil e o doador facilitou bastante.');

      cy.wait(5000);
      
      // Clicar no botão 'Concluir' e esperar a navegação
      cy.get('button').contains('Concluir').click();

      // Verificar se a navegação ocorreu corretamente
      cy.url().should('include', '/avaliacoes').then(() => {
        cy.log('Redirecionamento para /avaliacoes bem-sucedido');
      });
  });
});
