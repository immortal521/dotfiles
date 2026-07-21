let $autoload_path = $nu.default-config-dir | path join "autoload"

mkdir ($autoload_path)

$env.STARSHIP_CONFIG = ($env.HOME | path join ".config/starship/starship.toml")

let $nu_cfg_for_starship = $autoload_path | path join "starship.nu"
if (which starship | is-not-empty) {
    starship init nu | save -f $nu_cfg_for_starship
} else {
    if ($nu_cfg_for_starship | path exists) {
        rm $nu_cfg_for_starship
    }
}

let $nu_cfg_for_zoxide = $autoload_path | path join "zoxide.nu"
if (which zoxide | is-not-empty) {
    zoxide init nushell | save -f $nu_cfg_for_zoxide
} else {
    if ($nu_cfg_for_zoxide | path exists) {
        rm $nu_cfg_for_zoxide
    }
}

let nu_cfg_for_mise = $autoload_path | path join "mise.nu"

if (which mise | is-not-empty) {
    mise activate nu | save -f $nu_cfg_for_mise
} else {
    if ($nu_cfg_for_mise | path exists) {
        rm $nu_cfg_for_mise
    }
}
