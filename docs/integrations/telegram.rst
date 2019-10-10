
Telegram integration
========================

Any model specified by a DeepPavlov config can be launched as a Telegram bot.
You can do it using command line interface or using python.

Command line interface
~~~~~~~~~~~~~~~~~~~~~~

To run a model specified by the ``<config_path>`` config file as a telegram bot
with a ``<telegram_token>``:

.. code:: bash

    python -m deeppavlov interactbot <config_path> -t <telegram_token> [-d]


* ``-t <telegram_token>``: specifies telegram token as ``<telegram_token>``.
* ``-d``: downloads model specific data before starting the service.

The command will print the used host and port. Default web service properties
(host, port, model endpoint, GET request arguments) can be modified via changing
``deeppavlov/utils/settings/server_config.json`` file. Advanced API
configuration is described in :doc:`REST API </integrations/rest_api>` section.

If you want to get custom ``/start`` and ``/help`` Telegram messages for the running model you should:

* Add section to ``models_info`` section of ``deeppavlov/utils/settings/connector_config.json`` with your custom
  Telegram messages
* In model config file specify ``metadata.labels.telegram_utils`` parameter with name which
  refers to the added section of ``deeppavlov/utils/settings/models_info.json`` ``models_info`` section.

Python
~~~~~~

To run a model specified by a DeepPavlov config ``<config_path>`` as as
Telegram bot, you have to turn it to a :class:`~deeppavlov.deprecated.skill.skill.Skill`
and then make it an :class:`~deeppavlov.deprecated.agent.agent.Agent`.

.. code:: python

    from deeppavlov import build_model
    from deeppavlov.deprecated.skills.default_skill import DefaultStatelessSkill
    from deeppavlov.deprecated.agents.default_agent import DefaultAgent
    from deeppavlov.deprecated.agents.processors import HighestConfidenceSelector
    from deeppavlov.utils.telegram.telegram_ui import init_bot_for_model

    model = build_model("<config_path>", download=True)

    # Step 1: make it a Skill 
    skill = DefaultStatelessSkill(model)
    # Step 2: make it an Agent
    agent = DefaultAgent(skills=[skill])
    # Step 3: run server
    init_bot_for_model(agent, token="<telegram_token>", name="my_model_name")

If your model is already a subclass of :class:`~deeppavlov.deprecated.skill.skill.Skill`
or a subclass of :class:`~deeppavlov.deprecated.agent.agent.Agent` (see
:doc:`skills </apiref/skills>` and :doc:`agents </apiref/agents>`) you can skip
corresponding steps.

