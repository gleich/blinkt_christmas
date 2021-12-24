package conf

import (
	"os"
	"path/filepath"

	"github.com/gleich/lumber/v2"
	"github.com/pelletier/go-toml/v2"
)

// Read from the config file
func Read(log lumber.Logger) (Config, error) {
	log.Info("Loading configuration")

	// Configuration location
	homeDir, err := os.UserHomeDir()
	if err != nil {
		return Config{}, err
	}
	location := filepath.Join(homeDir, ".config", "blinkt_christmas", "conf.toml")

	// Reading the binary from the file
	b, err := os.ReadFile(location)
	if err != nil {
		return Config{}, err
	}

	// Parsing toml
	var data Config
	err = toml.Unmarshal(b, &data)
	if err != nil {
		return Config{}, err
	}

	// Validate config
	if data.Brightness == nil {
		defaultBrightness := 0.1
		data.Brightness = &defaultBrightness
	}
	if data.On == nil {
		defaultOnStatus := true
		data.On = &defaultOnStatus
	}

	log.Success("Loaded configuration")
	return data, nil
}
