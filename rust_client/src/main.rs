// use tokio::net::TcpStream;
// use tokio::io::AsyncWriteExt;
// use std::error::Error;
use std::env;
use openssl::ssl::{SslConnector, SslMethod, SslStream};
use std::io::{Read, Write};
use std::net::TcpStream;

// #[tokio::main]
// async fn main() -> Result<(), Box<dyn Error>> {
//     let host = match env::var("HOST") {
//         Ok(host) => host,
//         Err(_) => String::from("server"),
//     };

//     let port  = match env::var("PORT") {
//         Ok(port) => port,
//         Err(_) => String::from("8000"), 
//     };

//     let address = format!("{}:{}", host, port);

//     let mut stream = TcpStream::connect(address).await?;
//     println!("created stream");

//     stream.write_all(b"hello world\n").await?;

//     stream.readable().await?;
//     let mut buf = [0; 4096];

//     match stream.try_read(&mut buf) {
//         Ok(0) => {
//             println!("received: nothing");
//         },
//         Ok(n) => {
//             let response = String::from_utf8_lossy(&buf[..n]);
//             println!("received: {}", response);
//         },
//         Err(_) => {
//             println!("err reading buffer");
//         }
//     }

//     Ok(())
// }

fn main() {
    let host = match env::var("HOST") {
        Ok(host) => host,
        Err(_) => String::from("server"),
    };

    let port  = match env::var("PORT") {
        Ok(port) => port,
        Err(_) => String::from("8000"), 
    };

    let address = format!("{}:{}", host, port);

    let mut connector_builder = SslConnector::builder(SslMethod::tls()).unwrap();
    
    // disable verify
    // connector_builder.set_verify(openssl::ssl::SslVerifyMode::NONE);
    
    // use local cert file
    connector_builder.set_ca_file("/certs/cert.pem")
        .unwrap_or_else(|_| panic!("unable to load cert"));
    
    let connector = connector_builder.build();

    let mut configurator = connector.configure().unwrap();

    // disable hostname verify
    configurator.set_verify_hostname(false);

    let raw_stream = TcpStream::connect(address).unwrap();
    let mut stream = configurator.connect(&host, raw_stream).unwrap();

    stream.write_all(b"hello world").unwrap();
    
    // Read a fixed amount of data instead of reading until EOF
    let mut buffer = [0; 1024];
    let bytes_read = stream.read(&mut buffer).unwrap();
    let response = String::from_utf8_lossy(&buffer[..bytes_read]);
    println!("received: {}", response);
}