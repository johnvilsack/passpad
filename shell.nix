{
  pkgs ? import <nixpkgs> {}
}:

pkgs.mkShell {
  buildInputs = [
    pkgs.python311Full
    pkgs.python311Packages.tkinter
    pkgs.python311Packages.pyinstaller
  ];
}
