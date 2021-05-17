def ordination(routes):
    print('Iniciando ordenação da lista')

    numberMax = len(routes) ** 2
    isTrue = True
    count = 1

    loop = []

    while isTrue:  
        a = []

        for i in range(0, len(routes)):
            if (len(routes[i]['dependecies']) == 0):
                continue

            b = False

            for j in range(i+1, len(routes)):
                if (routes[j]['route'] in routes[i]['dependecies']):
                    b = True    
            
            if b:
                routes[i], routes[i+1] = routes[i+1], routes[i]

                loop.append(routes[i])
                a.append(True)   
            else:
                a.append(False)

        count += 1

        if True not in a:
            print('Lista ordenada!')
            isTrue = False

        if count == numberMax:
            print('Loop infinito. Configure corretamente a lista!')

            for i in loop: 
                print(i)
                
            isTrue = False
   
    return routes

#Rotas Service Layer
routes = [
    {
        'route': 'bairro',
        'dependecies': ['municipio'],
        'useable': False
    },
    {
        'route': 'logradouro',
        'dependecies': ['municipio', 'tipo-logradouro'],
        'useable': False
    },
    {
        'route': 'agencia-bancaria',
        'dependecies': ['banco', 'logradouro', 'bairro'],
        'useable': False
    },
    {
        'route': 'feriado',
        'dependecies': [],
        'useable': False
    },
    {
        'route': 'tipo-movimentacao-pessoal',
        'dependecies': ['campo-adicional'],
        'useable': False
    },
    {
        'route': 'motivo-alteracao-salarial',
        'dependecies': ['tipo-movimentacao-pessoal'],
        'useable': False
    },
    {
        'route': 'campo-adicional',
        'dependecies': [],
        'useable': False
    },
    {
        'route': 'configuracao-organograma',
        'dependecies': [],
        'useable': False
    },
    {
        'route': 'funcao',
        'dependecies': ['tipo-funcao', 'tipo-movimentacao-pessoal'],
        'useable': False
    },
    {
        'route': 'tipo-funcao',
        'dependecies': [],
        'useable': False
    },
    {
        'route': 'pessoa-fisica',
        'dependecies': ['pais', 'municipio', 'bairro', 'logradouro', 'agencia-bancaria', 'campo-adicional'],
        'useable': False
    }, 
    {
        'route': 'pessoa-juridica',
        'dependecies': ['pais', 'municipio', 'bairro', 'pessoa-fisica'],
        'useable': False
    },  
    {
        'route': 'ato',
        'dependecies': ['tipo-ato', 'natureza-texto-juridico', 'pessoa-fisica', 'fonte-divulgacao', 'campo-adicional'],
        'useable': False
    },
    {
        'route': 'fonte-divulgacao',
        'dependecies': [],
        'useable': False
    },
    {
        'route': 'natureza-texto-juridico',
        'dependecies': ['campo-adicional'],
        'useable': False
    },
    {
        'route': 'tipo-ato',
        'dependecies': ['campo-adicional'],
        'useable': False
    },
    {
        'route': 'organograma',
        'dependecies': ['configuracao-organograma', 'ato', 'pessoa-fisica', 'campo-adicional', 'funcao'],
        'useable': False
    },
    {
        'route': 'tipo-afastamento',
        'dependecies': ['campo-adicional', 'tipo-movimentacao-pessoal'],
        'useable': False
    },
    {
        'route': 'afastamento',
        'dependecies': ['tipo-afastamento', 'ato', 'matricula', 'campo-adicional'],
        'useable': True
    },
    {
        'route': 'motivo-rescisao',
        'dependecies': ['tipo-movimentacao-pessoal', 'tipo-afastamento'],
        'useable': False
    },
    {
        'route': 'base',
        'dependecies': [],
        'useable': False
    },
    {
        'route': 'tipo-cargo',
        'dependecies': ['tipo-movimentacao-pessoal', 'campo-adicional'],
        'useable': False
    },
    {
        'route': 'configuracao-cancelamento-ferias',
        'dependecies': ['tipo-afastamento'],
        'useable': False
    },
    {
        'route': 'categoria-trabalhador',
        'dependecies': [],
        'useable': False
    },
    {
        'route': 'vinculo-empregaticio',
        'dependecies': ['categoria-trabalhador', 'motivo-rescisao', 'campo-adicional'],
        'useable': False
    },
    {
        'route': 'movimentacao-pessoal',
        'dependecies': ['tipo-movimentacao-pessoal', 'matricula', 'ato'],
        'useable': True
    },
    {
        'route': 'grupo-funcional',
        'dependecies': [],
        'useable': False
    },
    {
        'route': 'configuracao-lotacao-fisica',
        'dependecies': [],
        'useable': False
    },
    {
        'route': 'lotacao-fisica',
        'dependecies': ['configuracao-lotacao-fisica'],
        'useable': False
    },
    {
        'route': 'configuracao-encargos-sociais',
        'dependecies': [],
        'useable': False
    },
    {
        'route': 'plano-cargo-salario',
        'dependecies': [],
        'useable': False
    },
    {
        'route': 'nivel-salarial',
        'dependecies': ['plano-cargo-salario', 'campo-adicional', 'ato', 'motivo-alteracao-salarial'],
        'useable': False
    },
    {
        'route': 'configuracao-ferias',
        'dependecies': ['configuracao-cancelamento-ferias'],
        'useable': False
    },
    {
        'route': 'plano-previdencia',
        'dependecies': ['ato'],
        'useable': False
    },
    {
        'route': 'horario',
        'dependecies': ['campo-adicional'],
        'useable': False
    },
    {
        'route': 'selecao-avancada',
        'dependecies': ['organograma', 'cargo', 'lotacao-fisica', 'matricula', 'grupo-funcional', 'vinculo-empregaticio'],
        'useable': True
    },
    {
        'route': 'matricula',
        'dependecies': ['motivo-alteracao-cargo', 'organograma', 'cargo', 'lotacao-fisica', 'nivel-salarial', 'grupo-funcional', 'vinculo-empregaticio', 'categoria-trabalhador', 'motivo-alteracao-salarial', 'campo-adicional'],
        'useable': False
    },
    {
        'route': 'classe-referencia',
        'dependecies': ['nivel-salarial'],
        'useable': False 
    },
    {
        'route': 'cargo',
        'dependecies': ['ato', 'tipo-cargo', 'configuracao-licenca-premio', 'configuracao-ferias', 'nivel-salarial', 'classe-referencia', 'campo-adicional'],
        'useable': False
    },
    {
        'route': 'configuracao-licenca-premio',
        'dependecies': [],
        'useable': False
    },
    {
        'route': 'configuracao-evento',
        'dependecies': ['ato', 'motivo-rescisao', 'campo-adicional'],
        'useable': False
    },
    {
        'route': 'configuracao-dirf',
        'dependecies': ['configuracao-evento'],
        'useable': False
    },
    {
        'route': 'lancamento-evento',
        'dependecies': ['matricula', 'configuracao-evento'],
        'useable': False
    },
    {
        'route': 'movimentacao-pessoal',
        'dependecies': ['matricula', 'tipo-movimentacao-pessoal', 'ato'],
        'useable': False
    },
    {
        'route': 'calculo-folha-mensal',
        'dependecies': ['matricula', 'configuracao-calculo'],
        'useable': True
    },
    {
        'route': 'calculo-folha-decimo-terceiro',
        'dependecies': ['matricula', 'configuracao-calculo', 'periodo-aquisitivo-decimo-terceiro'],
        'useable': True
    },
    {
        'route': 'calculo-folha-rescisao',
        'dependecies': ['matricula', 'ato', 'motivo-rescisao', 'configuracao-calculo', 'rescisao'],
        'useable': True
    },
    {
        'route': 'calculo-folha-ferias',
        'dependecies': ['configuracao-ferias', 'ato', 'tipo-afastamento', 'matricula', 'configuracao-calculo', 'periodo-aquisitivo-ferias'],
        'useable': True
    },
    {
        'route': 'folha',
        'dependecies': ['calculo-folha-ferias', 'calculo-folha-rescisao', 'calculo-folha-mensal', 'calculo-folha-decimo-terceiro', 'configuracao-evento', 'matricula'],
        'useable': True
    },
    {
        'route': 'rescisao',
        'dependecies': ['matricula', 'ato', 'motivo-rescisao', 'aviso-previo', 'configuracao-calculo'],
        'useable': True
    },
    {
        'route': 'motivo-alteracao-cargo',
        'dependecies': ['campo-adicional'],
        'useable': False
    },
    {
        'route': 'dependencia',
        'dependecies': ['pessoa-fisica'],
        'useable': True
    },
    {
        'route': 'configuracao-calculo',
        'dependecies': ['tipo-afastamento'],
        'useable': True
    },
    {
        'route': 'periodo-aquisitivo-decimo-terceiro',
        'dependecies': ['matricula', 'configuracao-calculo'],
        'useable': True
    },
    {
        'route': 'periodo-aquisitivo-ferias',
        'dependecies': ['matricula', 'tipo-afastamento', 'configuracao-ferias', 'configuracao-calculo'],
        'useable': True
    },
    {
        'route': 'servico-autonomo',
        'dependecies': ['matricula', 'cbo'],
        'useable': True
    },
    {
        'route': 'configuracao-rais',
        'dependecies': ['pessoa-juridica', 'pessoa-fisica'],
        'useable': True
    },
    {
        'route': 'configuracao-rais-campo',
        'dependecies': ['configuracao-evento'],
        'useable': True
    },
    {
        'route': 'averbacao-matricula',
        'dependecies': ['ato', 'matricula'],
        'useable': True
    },
    {
        'route': 'configuracao-adicional',
        'dependecies': ['tipo-afastamento'],
        'useable': True
    },
    {
        'route': 'configuracao-recrutamento',
        'dependecies': [],
        'useable': True
    },
    {
        'route': 'periodo-aquisitivo-licenca-premio',
        'dependecies': ['configuracao-licenca-premio', 'matricula', 'ato'],
        'useable': True
    }
]

#Faz a ordenação conforme dependencias
orderedRoutes = ordination(routes)