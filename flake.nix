{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system: 
      let
        pkgs = import nixpkgs { inherit system; };

        shell = with pkgs; mkShell {
          nativeBuildInputs = [
            python311
            python311Packages.pip
            python311Packages.virtualenv
          ];
          shellHook = ''
            virtualenv venv
            source venv/bin/activate
            pip install -r requirements.txt
          '';
        };
      in
      {
        devShells.default = shell;
      });
}
