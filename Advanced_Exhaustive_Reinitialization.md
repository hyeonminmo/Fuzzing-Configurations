# Advanced exhaustive reinitialization

## 0. Environment
- OS: ubuntu 20.04 LTS

## 1. Overview

![AdvExhReinitOverview](https://user-images.githubusercontent.com/3887348/167621236-19c4d543-e4be-47ea-af5e-8449d09319e3.png "AdvExhReinitOverview")

## 2. Extract variable edges and inputs (Pre-run: afl-fuzz with debug mode)

This step produces variable edges and variable inputs of a target program.

## 3. Extract (real) variable edges and inputs

This step produces real variable edges and inputs.

## 4. Do exhaustive reinitialization with the real variable edges and inputs


