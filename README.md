# Lectures on Modern Scientific Computing - Workshop

This repository contains the workshop support materials.
Please clone the repository by running the following command in your terminal:

```bash
git clone https://github.com/nata108/LMSC.git
```

## Task 1 - Clone TaskWeaver

To start using TaskWeaver, you need to clone the repository. You can do this by running the following command in your terminal:

```bash
git clone https://github.com/microsoft/TaskWeaver.git
```

Navigate to the TaskWeaver directory:

```bash
cd TaskWeaver
```

Then, install the required packages:

```bash
pip install -r requirements.txt
```

### Configuring TaskWeaver

To configure TaskWeaver navigate to the `project` directory and locate `taskweaver_config.json`.
You should add the following lines to the file:

```json
{
  "llm.api_base": "https://api.openai.com/v1",
  "llm.api_key": "<ADD YOUR API KEY HERE>",
  "llm.model": "gpt-4o-mini",
  "execution_service.kernel_mode": "local"
}
```

We will work with OpenAI's fastest model, `gpt-4o-mini`. The API key will be given during the workshop. Setting the kernel mode to `local` will allow the LLM agent to run code on your machine without setting up a complex development container environment (for production use, you should remove this).

For a webui installing chainlit is required. 

```bash
pip install -U "chainlit<1.1.300"
```

## Task 2 - Try the agentic workflow

To run the webUI, navigate to `playground/UI` and run the following command:

```bash
chainlit run app.py
```

Try experimenting with the agent, complete the following tasks (plus anything that comes to mind):

1. Ask the agent to solve a mathematical riddle using reasoning. For example: ```Infinitely many mathematicians walk into a bar. The first one orders a beer. The second orders half a beer. The third orders a quarter of a beer. The bartender says, "You're all idiots," and reaches for glasses. How many glasses of beer does the bartender pour?```
2. Ask the agent to analyze data for you attach sunspot data and ask a complex problem like ```Create a heat map of sunspots over years, months days where there are multiple observers that agree (to a degree) on the sunspot count.``` Watch how the agent progresses through the problem.
3. Ask the agent to perform an FDTD simulation. For example: ```Simulate a 2D FDTD simulation with a line detector and a point source, scatter rectangular objects in the simulation space and observe the wave propagation.``` Most likely the agent will fail.


## Task 3 - Enable FDTD simulation

Install plugin dependencies by navigating to the main folder and running:

```bash
pip install -r requirements_plugins.txt
```

Enable direct tool execution plugins by navigating to `project/plugins` and copying the `fdtd_sim.py` and `fdtd_sim.yaml` files there. Check the YAML config if the plugin is set to `enabled: true`.

After that restart the webUI and try the following FDTD simulation again.

Finally, try to ask the agent to plan the FDTD simulation parameters based on high-level or more obscure requirements.


## Task 4 - Finish and try the three-body simulator

Find the `threebody.py` and `threebody.yaml` files in the main folder and copy them to the `project/plugins` folder. Finish the code and description files and enable the plugin in the YAML config.

Tip: Ask the agent to fall back to default parameters for "less simple" solutions. Play around with requests related to placement and parametrization of the bodies.

## Optional Task 5 - Create your own plugin

Building on the examples provided come up with your own plugin. Find more details on plugins in: https://microsoft.github.io/TaskWeaver/docs/plugin/plugin_intro/
