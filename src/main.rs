extern crate clap;
extern crate subprocess;

mod parse;

use clap::App;
use parse::ParseError;
use std::collections::HashMap;
use std::fs::File;
use std::io::Read;
use std::path::Path;

#[derive(Clone, Debug, PartialEq)]
pub struct Call {
    name: String,
    args: Vec<String>,
}

impl Call {
    pub fn new<S: Into<String> + Clone>(name: S, args: Vec<S>) -> Call {
        Call {
            name: name.into(),
            args: args.iter().map(|a| (*a).clone().into()).collect()
        }
    }
}

#[derive(Clone, Debug, PartialEq)]
pub struct Directive(Vec<Call>);

#[derive(Clone, Debug, PartialEq)]
pub struct TargetHeader {
    name: String,
    calls: Vec<Call>,
}

impl TargetHeader {
    pub fn new<S: Into<String>>(name: S, calls: Vec<Call>) -> TargetHeader {
        TargetHeader { name: name.into(), calls: calls }
    }
}

#[derive(Clone, Debug, PartialEq)]
pub struct Command {
    directive: Option<Directive>,
    code: String,
}

impl Command {
    fn new<S: Into<String>>(directive: Option<Directive>, code: S) -> Command {
        Command { directive, code: code.into() }
    }
}

#[derive(Clone, Debug, PartialEq)]
pub struct Target {
    header: TargetHeader,
    commands: Vec<Command>,
}

impl Target {
    pub fn new(header: TargetHeader, commands: Vec<Command>) -> Target {
        Target { header: header, commands: commands }
    }

    pub fn name(&self) -> &str {
        &self.header.name
    }
}

#[derive(Clone, Debug, PartialEq)]
pub struct SateFile {
    path: String,
    targets: HashMap<String, Target>,
}

impl SateFile {
    fn new() -> SateFile {
        SateFile { path: "".to_string(), targets: HashMap::new() }
    }

    fn parse_string(text: &str) -> Result<SateFile, ParseError> {
        return parse::satefile(text);
    }

    fn parse_from_file(path: &Path) -> Result<SateFile, ParseError> {
        // TODO, remove unwrap()s
        let mut file = File::open(path).unwrap();
        let mut contents = String::new();
        file.read_to_string(&mut contents).unwrap();
        SateFile::parse_string(&contents)
    }

    fn add_target(&mut self, target: Target) {
        // TODO(nicholasbishop): handle duplicate targets better
        let name = target.header.name.clone();
        self.targets.insert(name, target);
    }

    fn run_target(&self, target_name: &str) {
        if let Some(target) = self.targets.get(target_name) {
            for command in target.commands.iter() {
                let res = subprocess::Exec::shell(&command.code).join();
                // TODO(nicholasbishop): better error handling
                if res.is_err() {
                    panic!("error: target failed");
                }
            }
        } else {
            println!("error: target '{}' does not exist", target_name);
        }
    }
}

fn print_targets(satefile: &SateFile) {
    for (name, _target) in satefile.targets.iter() {
        println!("{}", name);
    }
}

fn new_app<'a, 'b>() -> App<'a, 'b> {
    App::new("sate")
        .about("Run a task")
        .version("0.1.0")
        .args_from_usage(
            "-l, --list 'list all targets'
             [TARGET]   'name of target to execute'")
}

fn main() {
    // TODO(nicholasbishop): add command line option for file and
    // target
    let matches = new_app().get_matches();

    let default_path = Path::new(".satefile");
    // TODO(nicholasbishop): fix unwrap
    let satefile = SateFile::parse_from_file(default_path).unwrap();

    if matches.is_present("list") {
        print_targets(&satefile);
    } else if let Some(target) = matches.value_of("TARGET") {
        satefile.run_target(target);
    } else {
        println!("no target specified");
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_app() {
        let matches = new_app().get_matches_from(vec!["sate", "-l"]);
        assert!(matches.is_present("list"));
    }
}
