# Fileren

[PROJECT WEBSITE](https://hawier.dev/projects/other/fileren.html)

Simple tool for renaming files in a directory

![How to use gif](assets/how_to_use.gif)

## Installation

```shell
pip install fileren
```

## Usage

To run the program, simply run the following command:

```shell
fileren
```

Or run command with arguments:

```shell
fileren --path {path_to_directory} --regex {regex} --new_string {new_string}
```

To insert the current index of the file, use the following syntax as new string:

Example: 

```shell
fileren --path data --regex _text_[0-9]+ --new_string _{i}_
```

Input:

```shell
data
├── file_text_1.txt
├── file_text_2.txt
├── file_text_3.txt
└── file_text_4.txt
```

Output:

```shell
data
├── file_0.txt
├── file_1.txt
├── file_2.txt
└── file_3.txt
```

