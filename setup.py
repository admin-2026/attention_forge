from setuptools import setup, find_packages

setup(
    name="attention_forge",
    version="0.2.7",
    description="A tool for AI-assisted coding with automated file updates and backups.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-repo/attention_forge",
    packages=find_packages(include=["attention_forge", "attention_forge.*", "attention_forge.clients"]),
    include_package_data=True,
    package_data={
        "attention_forge": [
            "role_configs/*.yaml",
            "chain_configs/*.yaml",
            "setup_tools/plugins/*.py",  # Include plugins
            "api-keys/*.yaml"
        ],
    },
    install_requires=[
        "openai>=1.0.0",
        "pyyaml",
        "ollama>=0.4.7",
    ],
    python_requires=">=3.8",
)