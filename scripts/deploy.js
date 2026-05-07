const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {
  const TokenEscrow = await hre.ethers.getContractFactory("TokenEscrow");
  const escrow = await TokenEscrow.deploy();
  await escrow.waitForDeployment();

  const contractAddress = await escrow.getAddress();
  const artifact = await hre.artifacts.readArtifact("TokenEscrow");

  const deploymentInfo = {
    contractName: "TokenEscrow",
    address: contractAddress,
    abi: artifact.abi,
    network: hre.network.name,
    chainId: 31337,
    deployedAt: new Date().toISOString()
  };

  const deploymentDir = path.join(__dirname, "..", "deployments");
  if (!fs.existsSync(deploymentDir)) {
    fs.mkdirSync(deploymentDir, { recursive: true });
  }

  fs.writeFileSync(
    path.join(deploymentDir, "local.json"),
    JSON.stringify(deploymentInfo, null, 2),
    "utf-8"
  );

  console.log(`TokenEscrow deployed to: ${contractAddress}`);
  console.log("Deployment file written to deployments/local.json");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});

