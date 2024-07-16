# Query Your Video

![GitHub repo size](https://img.shields.io/github/repo-size/jungleBadger/qyv)
![GitHub contributors](https://img.shields.io/github/contributors/jungleBadger/qyv)
![GitHub stars](https://img.shields.io/github/stars/jungleBadger/qyv?style=social)
![GitHub forks](https://img.shields.io/github/forks/jungleBadger/qyv?style=social)
![GitHub issues](https://img.shields.io/github/issues/jungleBadger/qyv)
![GitHub license](https://img.shields.io/github/license/jungleBadger/qyv)

## Overview

A brief description of what your project does and its purpose.

## Stack

### Backend

- **Python 3.11**
- **Poetry**: Dependency manager
- **OpenCV**: Frame extraction
- **SwinLane Transformer**: Frame feature extraction
- **YOLOv5**: Frame object detection
- **MoviePy**: Audio extraction
- **PyDub**: Audio splitting
- **Librosa**: Audio chunk classification
- **PyMilvus**: Similarity Database connector

### Frontend

- **Node.js**: Server
- **Vue.js v3**: Frontend framework

## Diagrams

### Stack

![Stack diagram](./assets/stack_diagram.png)

### Pipelines Flow

![Pipelines flow diagram](./assets/flow_diagram.png)

## Installation and Usage

### Milvus instance

1. Execute Docker
2. Run the script [assets/infrastructure/milvus/standalone_embed.sh](assets/infrastructure/milvus/standalone_embed.sh)


### Backend Instructions

For specific instructions on how to install the dependencies and run the backend service, refer to the documentation linked below:

- [Backend Documentation](./service/README.md)

### Frontend Instructions

For specific instructions on how to install the dependencies, build the UI bundle, and execute it, refer to the documentation linked below:

- [Frontend Documentation](./ui/README.md)

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Project Link: [https://github.com/jungleBadger/qyv](https://github.com/jungleBadger/qyv)
