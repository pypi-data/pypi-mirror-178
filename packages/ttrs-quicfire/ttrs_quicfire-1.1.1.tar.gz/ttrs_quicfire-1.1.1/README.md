# ttrs_quicfire

ttrs_quicfire is a Python library to easily configure burn models for plots of land defined using shape files for the quicfire model.

## Installation

> **DISCLAIMER:** This is currently the only verified and supported installation method. Other methods may work but will not be troubleshooted by the authors.

1. Download and install anaconda [here](https://www.anaconda.com).
2. Start by downloading the fastfuels.yml from the GitHub [repo](https://github.com/QUIC-Fire-TT/ttrs_quicfire). This can also be done using:
    ```console
    (base) system:~ user$ wget https://raw.githubusercontent.com/QUIC-Fire-TT/ttrs_quicfire/main/fastfuels.yml
    ```
3. Navigate to where the fastfuels.yml is located and create a new conda enviornment using:
    ```console
    (base) system:~ user$ conda env create -f fastfuels.yml
    ```
4. Once the enviornment has been created, activate it using:
    ```console
    (base) system:~ user$ conda activate fastfuels
    ```
5. Next, install ttrs_quicfire using:
    ```console
    (fastfuels) system:~ user$ pip install ttrs_quicfire
    ```
    > **NOTE:** All additional packages will be installed with this step.

<hr>

ttrs_quicfire by Tall Timbers is licensed under a MIT License