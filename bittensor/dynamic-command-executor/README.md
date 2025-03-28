# Dynamic Command Executor

This project provides a simple command-line interface for dynamically executing the `btcli` command to register a wallet with specified parameters.

## Project Structure

```
dynamic-command-executor
├── src
│   ├── main.py
├── requirements.txt
└── README.md
```

## Installation

To install the required dependencies, run:

```
pip install -r requirements.txt
```

## Usage

To execute the command, use the following function in `main.py`:

```python
execute_command(wallet_name: str, hotkey_name: str, net_uid: str)
```

### Example

```python
execute_command("myWallet", "myHotkey", "12345")
```

This will execute the command:

```
btcli s register --wallet.name myWallet --hotkey myHotkey --netuid 12345
```

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.