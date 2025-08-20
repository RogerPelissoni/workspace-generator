# Tutorial de implementação
- Sistema desenvolvido e otimizado para utilização na Farm

## Etapa 1 - Gerar arquivos workspaces
- Execute o comando: node workspace-generator.js, o mesmo irá pedir dois caminhos, o primeiro refere-se a pasta onde ficarão os workspaces gerados, e a seguinte refere-se ao caminho ende estão os sistemas

## Etapa 2 - Configurando VSCode
- Instale a extensão Workspace Sidebar no VSCode
- Abra o arquivo de configurações do VSCode 'settings.json' e inclua as pastas de workspace desejadas:

```
"workspaceSidebar.rootFolders": [
    {
        "path": "C:\\Users\\roger\\Documents\\HGV\\WorkSpace\\apache_1"
    },
    {
        "path": "C:\\Users\\roger\\Documents\\HGV\\WorkSpace\\apache_2"
    },
],
```

## Etapa 3 - Gerenciador de Containers
- Execute o programa container_manager.exe, o mesmo tem o intuito de facilitar a documentação e acertividade ao navegar entre os containers
- Defina um título que seja dinâmico referente a 'demanada' que está sendo efetuada
- Defina o caminho, o mesmo devera conter o executável do apache, por exemplo:
```
C:\xampp\apache\bin\httpd.exe
```

## Etapa 4 - Criação de múltiplos apaches
- O recomendado é basicamente duplicar seu apache no <SEU USUÁRIO>/Apache24
- Para melhor separação e entendimento dos containers, é recomendado utilizar um sequencial na nomeação de pastas
```
Apache24, Apache24_2, Apache24_3...
htdocs, htdocs2, htdocs3...
```
- Ajuste as configuração referentes ao nome dado ao 'Apache24' e 'htdocs', presentes em Apache24/conf/httpd.conf
```
Define SRVROOT "c:/Users/<SEU USUÁRIO>/Apache24"
DocumentRoot "${SRVROOT}/htdocs"
<Directory "${SRVROOT}/htdocs">
```

## Etapa 5 - Feedback
- Seu feedback é muito importante para este projeto, caso necessite de alguma funcionalidade nova, não hesite em contatar roger@hgv.inf.br
