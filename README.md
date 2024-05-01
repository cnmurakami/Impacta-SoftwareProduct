# Impacta-SoftwareProduct
Repositório para as aulas de Software Product

# Integrantes
<table>
    <tr>
        <td>Caio Naoto Murakami</td>
        <td>2203207</td>
    </tr>
    <tr>
        <td>Ellen dos Santos Xavier</td>
        <td>2203485</td>
    </tr>
    <tr>
        <td>Rodrigo da Cunha de Assis</td>
        <td>2202934</td>
    </tr>
</table>

# Como utilizar

<p> Clone o repositório, monte o docker-compose e aguarde os containers iniciarem</p>

```powershell
docker-compose up
```

Após a inicialização dos serviços, o servidor poderá ser acessado através do localhost

```powershell
impacta-softwareproduct-app-1  |  * Serving Flask app 'server'
impacta-softwareproduct-app-1  |  * Debug mode: on
impacta-softwareproduct-app-1  | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
impacta-softwareproduct-app-1  |  * Running on all addresses (0.0.0.0)
impacta-softwareproduct-app-1  |  * Running on http://127.0.0.1:5000
impacta-softwareproduct-app-1  |  * Running on http://192.168.0.3:5000
impacta-softwareproduct-app-1  | Press CTRL+C to quit
impacta-softwareproduct-app-1  |  * Restarting with stat
impacta-softwareproduct-app-1  |  * Debugger is active!
impacta-softwareproduct-app-1  |  * Debugger PIN: 159-269-238
```

## Verificar o mysql

<p> No terminal do container db, execute os seguintes comandos:

```terminal
mysql -uroot -p
```

<p> Será solicitada a senha, que será <i>Unitario123</i>. <p>
<p> Uma vez inserida a senha, utilize o schema rscarautomotive

```terminal
use rscarautomotive
show tables
```

<!--
## Criar a imagem do docker
```powershell
docker image build -t nomedaimagem .
```

## Executar o docker
```powershell
docker run -p <port>:<port> -d nomedaimagem
```-->
