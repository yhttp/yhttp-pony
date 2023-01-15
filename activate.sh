# Pick first word of directory as venv name
HERE=`dirname "$(readlink -f "$BASH_SOURCE")"`
VENVSROOT=${HOME}/.virtualenvs

# If the first argument was not provided, use current directory name.
if [ -z "${1:-}" ]; then
  DIRNAME=$(basename ${HERE})
  VENVNAME=$(echo ${DIRNAME} | cut -d'-' -f1)
  VENV=${VENVSROOT}/${VENVNAME}
else
  VENV=${VENVSROOT}/${1:-}
fi


source ${VENV}/bin/activate
