from setuptools import setup, find_packages

setup(
    name="prompt_generator",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "PyQt5>=5.15.0",
    ],
    entry_points={
        "console_scripts": [
            "prompt_generator=prompt_generator:run_application",
        ],
    },
    author="Prompt Generator Team",
    description="Advanced Prompt Generator for L&D Professionals",
    keywords="prompt, generator, education, learning, development",
    python_requires=">=3.6",
)
