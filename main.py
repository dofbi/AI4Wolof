from pydantic_ai import Agent
from dotenv import load_dotenv

load_dotenv()

translation_agent = Agent(  
    "gemini-2.0-flash-exp",
    deps_type=dict,
    result_type=str,
    system_prompt=(
        'Vous êtes un traducteur expert en Wolof et Français. '
        'Votre rôle est de traduire des phrases du Wolof vers le Français. '
        'Vous devez fournir des traductions claires et précises pour chaque phrase.'
    ),
)


# Run the agent
result = translation_agent.run_sync('Jërejëf')
print(result.data)  
#> Merci.