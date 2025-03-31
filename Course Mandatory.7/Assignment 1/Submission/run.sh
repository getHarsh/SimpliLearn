#!/bin/bash
# Lending Club Loan Default Prediction - TensorFlow-Compatible Setup Script

# Constants
VENV_NAME=".venv"
NOTEBOOK_FILENAME="Lending_Club_Loan_Data_Analysis.ipynb"
LOG_FILE="setup_log.txt"
KERNEL_NAME="lending-club-env"

# Initialize log file
echo "--- Lending Club Setup Log $(date) ---" > "$LOG_FILE"

# Define color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Log functions
log() { 
  echo -e "${BLUE}[INFO]${NC} $1"
  echo "$(date +"%Y-%m-%d %H:%M:%S"): $1" >> "$LOG_FILE"
}

log_error() { 
  echo -e "${RED}[ERROR]${NC} $1"
  echo "ERROR: $(date +"%Y-%m-%d %H:%M:%S"): $1" >> "$LOG_FILE"
}

log_success() { 
  echo -e "${GREEN}[SUCCESS]${NC} $1"
  echo "SUCCESS: $(date +"%Y-%m-%d %H:%M:%S"): $1" >> "$LOG_FILE"
}

log_warning() { 
  echo -e "${YELLOW}[WARNING]${NC} $1"
  echo "WARNING: $(date +"%Y-%m-%d %H:%M:%S"): $1" >> "$LOG_FILE"
}

# Function to check if a command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Display header
echo ""
echo "================================================================================"
echo "========== Lending Club Loan Default Prediction - Setup & Run Script ==========="
echo "================================================================================"
echo ""

# Get script directory (where this script is located)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
log "Working in directory: $SCRIPT_DIR"

# Ensure requirements.txt exists
if [[ ! -f "requirements.txt" ]]; then
  log_error "requirements.txt not found in the current directory"
  exit 1
fi

# Check for available Python versions
log "Checking for Python installations..."

# Define compatible Python versions for TensorFlow (in order of preference)
COMPATIBLE_VERSIONS=("3.10" "3.11" "3.9" "3.8")

# Find all Python executables
PYTHON_PATHS=()
PYTHON_VERSIONS=()

# Check for Python versions managed by pyenv
if command_exists pyenv; then
  log "pyenv detected, checking for installed Python versions..."
  PYENV_VERSIONS=$(pyenv versions --bare 2>/dev/null | grep -E '^3\.(8|9|10|11)')
  if [[ -n "$PYENV_VERSIONS" ]]; then
    while IFS= read -r version; do
      log "Found pyenv Python $version"
      PYTHON_PATHS+=("$(pyenv which python$version 2>/dev/null)")
      PYTHON_VERSIONS+=("$version")
    done <<< "$PYENV_VERSIONS"
  fi
fi

# Check for Homebrew-installed Python versions
for version in "${COMPATIBLE_VERSIONS[@]}"; do
  if command_exists "python$version"; then
    PYTHON_PATHS+=("$(which python$version)")
    PYTHON_VERSIONS+=("$version")
    log "Found Python $version at $(which python$version)"
  elif [[ -f "/opt/homebrew/bin/python$version" ]]; then
    PYTHON_PATHS+=("/opt/homebrew/bin/python$version")
    PYTHON_VERSIONS+=("$version")
    log "Found Homebrew Python $version at /opt/homebrew/bin/python$version"
  elif [[ -f "/usr/local/bin/python$version" ]]; then
    PYTHON_PATHS+=("/usr/local/bin/python$version")
    PYTHON_VERSIONS+=("$version")
    log "Found Python $version at /usr/local/bin/python$version"
  fi
done

# Check system Python version
SYSTEM_PYTHON_VERSION=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
SYSTEM_PYTHON_MINOR=$(echo "$SYSTEM_PYTHON_VERSION" | cut -d. -f2)
if [[ $SYSTEM_PYTHON_MINOR -ge 8 && $SYSTEM_PYTHON_MINOR -le 11 ]]; then
  PYTHON_PATHS+=("$(which python3)")
  PYTHON_VERSIONS+=("3.$SYSTEM_PYTHON_MINOR")
  log "System Python $(python3 --version 2>&1) is compatible with TensorFlow"
else
  log_warning "System Python $(python3 --version 2>&1) is not compatible with TensorFlow"
fi

# If no compatible versions found
if [[ ${#PYTHON_PATHS[@]} -eq 0 ]]; then
  log_error "No Python version compatible with TensorFlow found (versions 3.8-3.11 required)"
  
  # Provide instructions based on the platform
  if [[ "$OSTYPE" == "darwin"* ]]; then
    log "On macOS, install a compatible Python version with Homebrew:"
    log "  brew install python@3.10"
    log "  brew link python@3.10"
  elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    log "On Linux, install a compatible Python version:"
    log "  sudo apt-get update && sudo apt-get install python3.10 python3.10-venv"
    log "  or"
    log "  sudo yum install python3.10 python3.10-devel"
  else
    log "Install Python 3.10 from https://www.python.org/downloads/"
  fi
  
  log_error "Please install a compatible Python version and run this script again"
  exit 1
fi

# Choose the first compatible Python version
PYTHON_PATH="${PYTHON_PATHS[0]}"
PYTHON_VERSION="${PYTHON_VERSIONS[0]}"
log_success "Using Python $PYTHON_VERSION at $PYTHON_PATH for TensorFlow compatibility"

# Function to get paths for the virtual environment
get_venv_python() {
  if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "${SCRIPT_DIR}/${VENV_NAME}/Scripts/python"
  else
    echo "${SCRIPT_DIR}/${VENV_NAME}/bin/python"
  fi
}

get_venv_pip() {
  if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "${SCRIPT_DIR}/${VENV_NAME}/Scripts/pip"
  else
    echo "${SCRIPT_DIR}/${VENV_NAME}/bin/pip"
  fi
}

get_venv_activate() {
  if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "${SCRIPT_DIR}/${VENV_NAME}/Scripts/activate"
  else
    echo "${SCRIPT_DIR}/${VENV_NAME}/bin/activate"
  fi
}

# Function to clean up processes on exit
cleanup_processes() {
  log "Cleaning up..."
  if [[ -n "$JUPYTER_PID" ]]; then
    log "Shutting down Jupyter server (PID: $JUPYTER_PID)..."
    kill -9 "$JUPYTER_PID" 2>/dev/null || true
  fi
}

# Set up trap to ensure clean exit
trap cleanup_processes EXIT INT TERM

# Create and set up virtual environment
log "Setting up virtual environment..."
VENV_PATH="${SCRIPT_DIR}/${VENV_NAME}"

# Remove existing virtual environment if it exists
if [[ -d "$VENV_PATH" ]]; then
  log "Removing existing virtual environment..."
  rm -rf "$VENV_PATH"
fi

# Create new virtual environment using the compatible Python version
log "Creating virtual environment at $VENV_PATH using Python $PYTHON_VERSION..."
"$PYTHON_PATH" -m venv "$VENV_PATH"

if [[ $? -ne 0 ]]; then
  log_error "Failed to create virtual environment"
  log "Checking if venv module is available..."
  
  if ! "$PYTHON_PATH" -c "import venv" &>/dev/null; then
    log_error "The venv module is not available for your Python installation"
    
    # Try to install venv if missing (platform specific)
    if [[ "$OSTYPE" == "darwin"* ]] && command_exists brew; then
      log "Installing Python venv support via Homebrew..."
      brew install python-tk@${PYTHON_VERSION}
      # Try again to create the virtual environment
      "$PYTHON_PATH" -m venv "$VENV_PATH"
    elif [[ "$OSTYPE" == "linux-gnu"* ]] && command_exists apt-get; then
      log "Installing Python venv support via apt..."
      sudo apt-get update && sudo apt-get install -y python3-venv
      # Try again to create the virtual environment
      "$PYTHON_PATH" -m venv "$VENV_PATH"
    fi
    
    # Check if venv creation succeeded after installation attempt
    if [[ ! -d "$VENV_PATH" || ! -f "$(get_venv_python)" ]]; then
      log_error "Failed to create virtual environment after attempting to install required packages"
      log_error "Please make sure you have the necessary packages for creating virtual environments"
      exit 1
    fi
  else
    log_error "Failed to create virtual environment for an unknown reason"
    exit 1
  fi
fi

log_success "Virtual environment created successfully"

# Get virtual environment Python and pip paths
VENV_PYTHON=$(get_venv_python)
VENV_PIP=$(get_venv_pip)
VENV_ACTIVATE=$(get_venv_activate)

# Verify that the virtual environment executables exist
if [[ ! -f "$VENV_PYTHON" ]]; then
  log_error "Python executable not found in the virtual environment"
  exit 1
fi

if [[ ! -f "$VENV_PIP" ]]; then
  log_error "Pip executable not found in the virtual environment"
  exit 1
fi

# Log Python version in the virtual environment
VENV_PYTHON_VERSION=$("$VENV_PYTHON" --version 2>&1)
log "Virtual environment Python version: $VENV_PYTHON_VERSION"

# Upgrade pip and install setuptools
log "Upgrading pip and installing setuptools..."
"$VENV_PIP" install --upgrade pip setuptools wheel >> "$LOG_FILE" 2>&1
if [[ $? -ne 0 ]]; then
  log_error "Failed to upgrade pip and install setuptools"
else
  log_success "Pip upgraded successfully"
fi

# Install TensorFlow first to ensure compatibility
log "Installing TensorFlow..."
if [[ "$OSTYPE" == "darwin"* ]] && [[ $(uname -m) == "arm64" ]]; then
  log "Detected Mac with M-series chip, installing TensorFlow for Metal..."
  "$VENV_PIP" install tensorflow-macos >> "$LOG_FILE" 2>&1
  if [[ $? -ne 0 ]]; then
    log_warning "Failed to install tensorflow-macos. Trying standard TensorFlow..."
    "$VENV_PIP" install tensorflow==2.13.0 >> "$LOG_FILE" 2>&1
    TF_INSTALL_RESULT=$?
  else
    TF_INSTALL_RESULT=0
  fi
else
  "$VENV_PIP" install tensorflow==2.13.0 >> "$LOG_FILE" 2>&1
  TF_INSTALL_RESULT=$?
  
  if [[ $TF_INSTALL_RESULT -ne 0 ]]; then
    log_warning "Failed to install TensorFlow 2.13.0. Trying a more compatible version..."
    "$VENV_PIP" install "tensorflow<2.14" >> "$LOG_FILE" 2>&1
    TF_INSTALL_RESULT=$?
  fi
fi

# Verify TensorFlow installation
"$VENV_PYTHON" -c "import tensorflow as tf; print(f'TensorFlow version: {tf.__version__}')" >> "$LOG_FILE" 2>&1
if [[ $? -ne 0 ]]; then
  log_error "TensorFlow installation verification failed"
  log_error "The environment will not work correctly for this notebook"
  exit 1
else
  log_success "TensorFlow installed and verified successfully"
fi

# Install compatible traitlets version first (fixes 'No module named jupyter_server.contents' error)
log "Installing compatible traitlets version..."
"$VENV_PIP" install traitlets==5.9.0 >> "$LOG_FILE" 2>&1
if [[ $? -ne 0 ]]; then
  log_warning "Failed to install compatible traitlets version - notebook may not work correctly"
else
  log_success "Installed traitlets 5.9.0 successfully"
fi

# Install specific IPython version compatible with traitlets 5.9.0
log "Installing compatible IPython version..."
"$VENV_PIP" install ipython==7.34.0 >> "$LOG_FILE" 2>&1
if [[ $? -ne 0 ]]; then
  log_warning "Failed to install compatible IPython version"
else
  log_success "Installed IPython 7.34.0 successfully"
fi

# Install Jupyter components with specific versions for compatibility
log "Installing Jupyter components with specific versions..."
"$VENV_PIP" install jupyter_server==1.23.4 notebook==6.5.4 jupyter_core==4.12.0 nbclassic==0.5.3 ipykernel==6.21.0 >> "$LOG_FILE" 2>&1
if [[ $? -ne 0 ]]; then
  log_error "Failed to install compatible Jupyter components"
  exit 1
else
  log_success "Jupyter components installed successfully"
fi

# Register the virtual environment with Jupyter
log "Registering virtual environment with Jupyter..."
"$VENV_PYTHON" -m ipykernel install --user --name="$KERNEL_NAME" --display-name="Python (Lending Club)" >> "$LOG_FILE" 2>&1
if [[ $? -ne 0 ]]; then
  log_error "Failed to register Jupyter kernel"
  exit 1
else
  log_success "Jupyter kernel registered successfully"
fi

# Install remaining dependencies from requirements.txt
log "Installing remaining dependencies from requirements.txt..."
grep -v "^python\|tensorflow\|jupyter\|notebook\|ipykernel" requirements.txt > requirements_filtered.txt
"$VENV_PIP" install -r requirements_filtered.txt >> "$LOG_FILE" 2>&1
INSTALL_RESULT=$?

# Clean up temporary file
rm -f requirements_filtered.txt

# Even if some packages fail, we continue if core packages are installed
if [[ $INSTALL_RESULT -ne 0 ]]; then
  log_warning "Some packages from requirements.txt could not be installed"
  log "Installing core packages individually to ensure functionality..."
  
  CORE_PACKAGES=("numpy" "pandas" "matplotlib" "seaborn" "scikit-learn")
  for pkg in "${CORE_PACKAGES[@]}"; do
    log "Installing $pkg..."
    "$VENV_PIP" install "$pkg" >> "$LOG_FILE" 2>&1
    if [[ $? -ne 0 ]]; then
      log_error "Failed to install $pkg"
    else
      log_success "Installed $pkg"
    fi
  done
else
  log_success "All dependencies installed successfully"
fi

# Create a simple TensorFlow test script
log "Testing TensorFlow installation..."
cat > tf_test.py << EOL
import tensorflow as tf
print(f"TensorFlow version: {tf.__version__}")
print("TensorFlow is working correctly")
EOL

# Run the test script
"$VENV_PYTHON" tf_test.py
if [[ $? -ne 0 ]]; then
  log_error "TensorFlow test failed"
  rm -f tf_test.py
  exit 1
else
  log_success "TensorFlow test successful"
  rm -f tf_test.py
fi

# Find dataset
log "Looking for dataset..."
DATASET_PATHS=(
  "${SCRIPT_DIR}/loan_data.csv"
  "${SCRIPT_DIR}/../../Datasets_October/Lending_Club_Data_Analysis_dataset/loan_data.csv"
  "${SCRIPT_DIR}/../Datasets_October/Lending_Club_Data_Analysis_dataset/loan_data.csv"
  "${SCRIPT_DIR}/../data/loan_data.csv"
  "${SCRIPT_DIR}/data/loan_data.csv"
  "${SCRIPT_DIR}/../datasets/loan_data.csv"
)

DATASET_PATH=""
for path in "${DATASET_PATHS[@]}"; do
  if [[ -f "$path" ]]; then
    if command_exists realpath; then
      DATASET_PATH=$(realpath "$path")
    else
      DATASET_PATH="$path"
    fi
    log_success "Dataset found: $path"
    break
  fi
done

if [[ -z "$DATASET_PATH" ]]; then
  log_error "Dataset not found in any of the expected locations"
  log "Using default path, but notebook may not work correctly"
  DATASET_PATH="${SCRIPT_DIR}/loan_data.csv"
fi

# Set environment variable for dataset path
export LENDING_CLUB_DATASET="$DATASET_PATH"
log "Set environment variable LENDING_CLUB_DATASET=$DATASET_PATH"

# Verify notebook file exists
log "Checking for notebook file: $NOTEBOOK_FILENAME"
if [[ ! -f "$NOTEBOOK_FILENAME" ]]; then
  log_warning "Notebook file not found: $NOTEBOOK_FILENAME"
  
  # Try to find any notebook file with .ipynb extension
  shopt -s nullglob
  NOTEBOOK_FILES=( *.ipynb )
  shopt -u nullglob
  
  if (( ${#NOTEBOOK_FILES[@]} > 0 )); then
    NOTEBOOK_FILENAME="${NOTEBOOK_FILES[0]}"
    log_success "Using available notebook: $NOTEBOOK_FILENAME"
  else
    log_error "No notebook files found. Cannot continue."
    exit 1
  fi
else
  log_success "Notebook file found: $NOTEBOOK_FILENAME"
fi

# Start Jupyter notebook server
log "Starting Jupyter notebook server for $NOTEBOOK_FILENAME..."
cd "$SCRIPT_DIR"

# Activate the virtual environment
if [[ -f "$VENV_ACTIVATE" ]]; then
  log "Activating virtual environment..."
  source "$VENV_ACTIVATE"
fi

# Start Jupyter notebook
log "Starting Jupyter with Lending Club kernel..."
jupyter notebook "$NOTEBOOK_FILENAME" --kernel="$KERNEL_NAME" &
JUPYTER_PID=$!
log "Started Jupyter notebook process with PID: $JUPYTER_PID"

# Wait a few seconds for Jupyter to start
log "Waiting for Jupyter server to start..."
sleep 3

# Keep the script running until Jupyter is terminated
log "Jupyter is running. Press Ctrl+C to terminate."
wait $JUPYTER_PID

log_success "Session completed"
exit 0