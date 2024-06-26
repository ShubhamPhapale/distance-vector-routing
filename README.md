# Dynamic Network Routing Simulation

This Python script simulates dynamic network routing using the Distance Vector Routing algorithm. It allows for changes in network topology over time and updates routing tables accordingly.

## Prerequisites

- Python 3.x
- Required Python packages: `queue`

## Usage

1. Clone this repository to your local machine by running:

    ```
    git clone https://github.com/ShubhamPhapale/distance-vector-routing/tree/main
    ```

2. Ensure you have Python 3.x installed.
3. Install the required Python package by running:
    ```
    pip install queue
    ```
4. Place your network topology configuration in `input.txt` and any dynamic changes in `change.txt`.
5. Run the simulation by executing the following command in your terminal:

    ```
    python dvrDynamicChanges.py
    ```

## Additional Resources

- [YouTube Video](https://youtu.be/7Qn09daLSJY)
- [My YouTube Channel](https://www.youtube.com/channel/UCzOmg9hOy3NBsScX--Nrb5Q)

## File Contents

### `input.txt`

The `input.txt` file should contain the initial network topology configuration. It should have the following format:

`<num_routers>`  
`<space-separated list of router names>`  
`<src>` `<dest>` `<cost>`  
`<src>` `<dest>` `<cost>`  
`...`  
`EOF`

Example:  
3  
A B C  
A B 2  
B C 3  
C A 4  
EOF

### `change.txt`

The `change.txt` file contains dynamic changes in the network topology. It should have the following format:

`<src>` `<dest>` `<cost>` `<timestamp>`    
`<src>` `<dest>` `<cost>` `<timestamp>`    
`...`

Example:  
A B 5 10  
B C 2 15

## Note

If the `change.txt` file is  empty, the program will run with the initial network configuration provided in `input.txt`.

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Added some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
