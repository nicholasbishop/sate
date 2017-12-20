extern crate clap;

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
        if let Some(_target) = self.targets.get(target_name) {
            println!("pretending to run {}", _target.name());
        } else {
            println!("error: target '{}' does not exist", target_name);
        }
    }
}

mod parse {
    include!(concat!(env!("OUT_DIR"), "/sate.rs"));
}

fn print_targets(satefile: &SateFile) {
    for (name, _target) in satefile.targets.iter() {
        println!("{}", name);
    }
}

fn main() {
    // TODO(nicholasbishop): add command line option for file and
    // target
    let matches = App::new("sate")
        .about("Run a task")
        .version("0.1.0")
        .args_from_usage(
            "-l, --list 'list all targets'
             [TARGET]   'name of target to execute'")
        .get_matches();

    let default_path = Path::new(".satefile");
    // TODO(nicholasbishop): fix unwrap
    let satefile = SateFile::parse_from_file(default_path).unwrap();

    if matches.is_present("list") {
        print_targets(&satefile);
    } else if let Some(target) = matches.value_of("TARGET") {
        satefile.run_target(target);
    }
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ident() {
        assert_eq!(parse::ident("abc").unwrap(), "abc");
        assert_eq!(parse::ident("abc123").unwrap(), "abc123");
        assert!(parse::ident("123").is_err());
    }

    #[test]
    fn test_arg_list() {
        assert_eq!(parse::arg_list("a b c").unwrap(), vec!["a", "b", "c"]);
    }

    #[test]
    fn test_call() {
        assert_eq!(parse::call("a()").unwrap(), Call::new("a", vec![]));
        assert_eq!(parse::call("a(b cd)").unwrap(), Call::new("a", vec!["b", "cd"]));
    }

    #[test]
    fn test_tag_directive() {
        assert_eq!(parse::tag_directive("[a()]").unwrap(),
                   Directive(vec![Call::new("a", vec![])]));
    }

    #[test]
    fn test_tag_target_simple() {
        assert_eq!(parse::tag_target_header("[a]").unwrap(),
                   TargetHeader::new("a", vec![]));
    }

    #[test]
    fn test_tag_target_with_call() {
        assert_eq!(parse::tag_target_header("[a b()]").unwrap(),
                   TargetHeader::new("a", vec![Call::new("b", vec![])]));
    }

    #[test]
    fn test_command() {
        assert_eq!(parse::command("a\n").unwrap(), Command::new(None, "a"));
        assert!(parse::command("[a]\n").is_err());
    }

    #[test]
    fn test_target() {
        assert_eq!(parse::target("[a]\nfoo\n").unwrap(),
                   Target::new(
                       TargetHeader::new("a", vec![]),
                       vec![Command::new(None, "foo")]));
    }

    #[test]
    fn test_satefile() {
        let mut satefile = SateFile::new();
        satefile.add_target(Target::new(
            TargetHeader::new("a", vec![]),
            vec![Command::new(None, "b")]));
        satefile.add_target(Target::new(
            TargetHeader::new("c", vec![]),
            vec![Command::new(None, "d")]));
        assert_eq!(
            parse::satefile("[a]\nb\n\n[c]\nd\n").unwrap(),
            satefile);
    }
}
