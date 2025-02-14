document.addEventListener("DOMContentLoaded", () => {
  const navToggle = document.getElementById("nav-toggle");
  const navLinks = document.getElementById("nav-links");

  navToggle.addEventListener("click", () => {
    navLinks.classList.toggle("show");
  });

  const terminalInput = document.getElementById("terminal-input");
  const terminalOutput = document.getElementById("terminal-output");

  terminalInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      const command = terminalInput.value.trim();
      terminalOutput.innerHTML += `<p>$ ${command}</p>`;

      // Simulate bot response
      if (command === "help") {
        terminalOutput.innerHTML += "<p>Available commands: help, about, exit</p>";
      } else {
        terminalOutput.innerHTML += `<p>Unknown command: ${command}</p>`;
      }

      terminalInput.value = "";
      terminalOutput.scrollTop = terminalOutput.scrollHeight;
    }
  });
});

const terminalInput = document.getElementById("terminal-input");
const terminalOutput = document.getElementById("terminal-output");

const commands = {
  help: "Supported commands: help, about, exit, uptime, disk, memory, cpu, ping <hostname>, netstat, scan",
  about: "KaliDev Security Bot - Comprehensive server management tool.",
  exit: "Clearing terminal...",
  uptime: "Fetching uptime...",
  disk: "Fetching disk usage...",
  memory: "Fetching memory usage...",
  cpu: "Fetching CPU usage...",
  netstat: "Fetching network statistics...",
  scan: "Starting security scan...",
};

terminalInput.addEventListener("keydown", async (e) => {
  if (e.key === "Enter") {
    const command = terminalInput.value.trim();
    const output = document.createElement("p");
    output.textContent = `$ ${command}`;
    terminalOutput.appendChild(output);

    if (command in commands) {
      const response = document.createElement("p");
      response.textContent = commands[command];
      terminalOutput.appendChild(response);

      if (["uptime", "disk", "memory", "cpu", "netstat", "scan"].includes(command)) {
        const result = await fetchCommandResult(command);
        const resultOutput = document.createElement("p");
        resultOutput.textContent = result || "Error fetching command output.";
        terminalOutput.appendChild(resultOutput);
      }
    } else if (command.startsWith("ping ")) {
      const host = command.split(" ")[1];
      const pingResult = await fetchCommandResult(`ping ${host}`);
      const resultOutput = document.createElement("p");
      resultOutput.textContent = pingResult || `Unable to ping ${host}.`;
      terminalOutput.appendChild(resultOutput);
    } else {
      const error = document.createElement("p");
      error.textContent = `Command "${command}" not recognized.`;
      terminalOutput.appendChild(error);
    }

    if (command === "exit") {
      terminalOutput.innerHTML = `<p class="typing-effect">Welcome back to KaliDev Security Bot!</p><p>$ Type "help" for options...</p>`;
    }

    terminalInput.value = "";
    terminalOutput.scrollTop = terminalOutput.scrollHeight;
  }
});

async function fetchCommandResult(command) {
  try {
    const response = await fetch(`/api/command`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ command }),
    });
    const data = await response.json();
    return data.result;
  } catch (err) {
    console.error("Error fetching command result:", err);
    return null;
  }
}
