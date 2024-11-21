Sistema de Comunicação Distribuída com Middleware
Descrição do Projeto

Este projeto implementa uma aplicação distribuída composta por três partes principais: Servidor, Middleware e Cliente. O sistema permite a comunicação entre clientes, utilizando o middleware como intermediário para gerenciar registros e localizar destinatários.

Funcionalidades

    Registro de Clientes: Os clientes se registram no middleware, que mantém informações como IP e porta.
    Busca de Destinatários: O middleware localiza destinatários registrados no sistema.
    Envio de Mensagens: Comunicação eficiente via protocolo UDP entre clientes.
    Alternância de Servidores: O middleware alterna entre servidores para garantir disponibilidade.

Arquitetura do Sistema

O sistema é composto por três componentes:

    Servidor
        Gerencia os registros de clientes.
        Oferece suporte para busca de destinatários.

    Middleware
        Atua como intermediário, alternando entre servidores.
        Impede o contato direto entre cliente e servidor.

    Cliente
        Permite registro no middleware.
        Envia mensagens para outros clientes via UDP.
        Escuta mensagens recebidas.

Tecnologias Utilizadas

    Python: Linguagem principal para desenvolvimento.
    Bibliotecas Nativas:
        socket: Comunicação em rede (TCP/UDP).
        threading: Gerenciamento de conexões simultâneas.
        json: Manipulação de dados estruturados.

Contribuições
Mauricio Gomes Rocha
Pedro Luna
