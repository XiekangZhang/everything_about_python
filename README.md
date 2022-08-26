# everything_about_python

pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U

conda update --all

conda env update --name myenv --file local.yml --prune
