use std::thread;
use chrono::prelude::*;
use paho_mqtt::Message;

fn main() {
    println!("Starting throughput test");

    let local = Local::now().timestamp_millis();
    println!("Begining a 15 second burst test.");
    let count = throughput_test(local, 15000);
    let bandwidth = count * 4;
    println!("{} msgs per minute", bandwidth);
}

fn throughput_test(start_time: i64, duration: i64) -> i32 {
    let end_time = start_time + duration;
    let mut msg_count = 0;
    let client = paho_mqtt::Client::new("tcp://192.168.0.150:1883")
        .expect("Error creating the MQTT Client");

    let _client_con = client.connect(Option::None)
        .expect("Error when establishing connection to the server specified");

    let msg = Message::new("testing/1", "t", 0);

    while Local::now().timestamp_millis() <= end_time {
        client.publish(msg.clone())
            .expect("Error when sending message to MQTT server");
        msg_count += 1;
    }
    msg_count
}
