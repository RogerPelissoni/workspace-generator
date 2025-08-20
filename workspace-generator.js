const fs = require("fs");
const path = require("path");
const readline = require("readline");

// Cria interface para entrada de dados
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

function perguntar(texto) {
  return new Promise((resolve) => {
    rl.question(texto, (resposta) => resolve(resposta.trim()));
  });
}

function normalizePath(path) {
  return path.replace(/\\/g, "/");
}

// Função principal
async function main() {
  const baseDir = await perguntar("Digite o caminho para o diretório de destino: ");
  const systemsDir = await perguntar("Digite o caminho para o caminho onde estão os sistemas HGV: ");

  // Cria pasta base se não existir
  if (!fs.existsSync(baseDir)) {
    fs.mkdirSync(baseDir, { recursive: true });
    console.log(`📁 Pasta criada: ${baseDir}`);
  }

  // Lê subpastas de systemsDir
  const arrSystems = fs.readdirSync(systemsDir).filter((item) => {
    const itemPath = path.join(systemsDir, item);
    return fs.statSync(itemPath).isDirectory();
  });

  // Cria arquivos para cada sistema
  for (const nmSystem of arrSystems) {
    const fileName = `${nmSystem}.code-workspace`;
    const fullPath = path.join(baseDir, fileName);

    const workspaceContent = `
    {
      "folders": [
          {
            "path": "${systemsDir}/${nmSystem}"
          }
      ],
      "settings": {
          "php.workspace.includePath": "${systemsDir}/padrao;${systemsDir}/padraomvc;${systemsDir}/padraoauxiliar",
          "intelephense.environment.includePaths": [
            "${systemsDir}/padraomvc",
            "${systemsDir}/padrao",
            "${systemsDir}/padraoauxiliar"
          ]
      }
    }`;

    fs.writeFileSync(fullPath, normalizePath(workspaceContent.trim()));
    console.log(`✅ Arquivo criado: ${fileName}`);
  }

  rl.close();
}

main();
