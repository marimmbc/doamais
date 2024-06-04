describe('Teste de agendamento de solicitação recebida', () => {
    it('Deve permitir ao usuário agendar a entrega de um item solicitado', () => {
      // Visitar a página inicial e clicar em "Entrar"
      cy.visit('http://127.0.0.1:8000/'); // Substitua pela URL correta
      cy.get('button').contains('Entrar').click();
  
      // Preencher o formulário de login e submeter
      cy.get('input#username').type('mmbc');
      cy.get('input#password').type('mari1402');
      cy.get('button').contains('Entrar').click();
  
      // Selecionar a opção 'Solicitações Recebidas' na navbar
      cy.get('a').contains('Solicitações Recebidas').click();
  
      // Esperar 5 segundos
      cy.wait(5000); // Espera 5 segundos
  
      // Clicar no botão 'Agendar' para o item 'Carro de Brinquedo'
      cy.get('tr').contains('Carro de Brinquedo').parent().find('button').contains('Agendar').click();
  
      // Preencher os campos de agendamento
      cy.get('input#hora_agendamento').type('16:45');
      cy.get('input#data_agendamento').type('2024-06-06');
  
      // Esperar 5 segundos
      cy.wait(5000); // Espera 5 segundos
  
      // Clicar no botão 'Agendar'
      cy.get('button').contains('Agendar').click();
    });
  });
  