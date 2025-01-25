package config

import (
	"errors"
	"io/fs"

	"github.com/caarlos0/env/v9"
	"github.com/joho/godotenv"
)

var Config = struct {
	Database      string `env:"POSTGRES_URI,notEmpty"`
	Port          int    `env:"PORT,notEmpty"`
	AdminUsername string `env:"ADMIN_USERNAME,notEmpty"`
	AdminPassword string `env:"ADMIN_PASSWORD,notEmpty"`
	Depth         int    `env:"DEPTH,notEmpty"`
	IsTestnet     bool   `env:"IS_TESTNET,notEmpty"`
	DataDir       string
	Toncenter     string
}{}

func LoadConfig() {
	err := godotenv.Load()
	if err != nil && !errors.Is(err, fs.ErrNotExist) {
		panic(err)
	}
	if err := env.Parse(&Config); err != nil {
		panic(err)
	}
	if Config.IsTestnet {
		Config.Toncenter = "https://testnet.toncenter.com/api/v2/"
	} else {
		Config.Toncenter = "https://toncenter.com/api/v2/"
	}
    Config.DataDir = "/api/apidata"
}
