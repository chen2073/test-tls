use tokio::net::TcpStream;
use tokio::io::AsyncWriteExt;
use std::error::Error;
use std::env;

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let host = match env::var("HOST") {
        Ok(host) => host,
        Err(_) => String::from("server"),
    };

    let port  = match env::var("PORT") {
        Ok(port) => port,
        Err(_) => String::from("8000"), 
    };

    let address = format!("{}:{}", host, port);

    let mut stream = TcpStream::connect(address).await?;
    println!("created stream");

    stream.write_all(b"hello world\n").await?;

    stream.readable().await?;
    let mut buf = [0; 4096];

    match stream.try_read(&mut buf) {
        Ok(0) => {
            println!("received: nothing");
        },
        Ok(n) => {
            let response = String::from_utf8_lossy(&buf[..n]);
            println!("received: {}", response);
        },
        Err(_) => {
            println!("err reading buffer");
        }
    }

    Ok(())
}