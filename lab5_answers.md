1. Three things that are visible in the plaintext capture and invisible in the TLS capture is the MQTT topic name,
   sensor value, and the protocol message structure. In the plaintext capture, you can clearly see the topic name string
   sensor/data. In the TLS capture, this is encrypted and replaced by random characters. Regarding the sensor value, you can
   see the specific temperature readings (temp:20C, temp:21C) in plaintext. In the TLS version, these values are scrambled and
   unreadable. The Protocol Message Structure: In plaintext, you can see exactly where the payload begins and ends. In the TLS
   capture, even the length and structure of the application data are obscured behind the TLS record layer.

   For an attacker, without TLS, they would be able to read every piece of data sent by the sensors. They would know exactly    what is happening in the monitored environment. By seeing the topic sensor/data, the attacker can learn the internal         logic of your IoT system, making it easier to plan a more targeted attack. Due to the fact that data is unencrypted, an attacker could not only read the data, but potentially inject fake data to trigger alerts or shut down systems without the broker or the Pi ever knowing the data was changed. With TLS, the attacker only sees that something is being sent to port 8883, but they have no way of knowing what the data is or how to manipulate it effectively.

3. When require_certificate is set to true, the broker enforces Mutual TLS. This means the connection will fail immediately if
   a client tries to connect without a valid certificate. The error received was Error: Protocol error. This error is
   mosquitto_sub saying the connection failed due to a TLS mismatch. The command did not provide any certificates. The VM has
   require_certificate true, it saw a connection attempt that didn't provide a client certificate and immediately cut the link.
   By setting allow_anonymous false and requiring certificates, this implements Mutual Authentication. This ensures that only 
   authorized users/hardware can talk to the server, and keeps all the communication encrypted.

4. One of the things Suricata can still observe is Server Name Indication and certificates. During the initial handshake, the
   client and server exchange some information in the clear. Suricata sees the hostname the client is trying to reach and the
   SSL/TLS certificate the server presents. This can be used to detect a threat by writing a rule to alert if a client connects
   to a "known-bad" domain or if the server presents a self-signed or expired certificate that doesn't match the lab's CA.
   This helps detect Man-in-the-Middle attacks. Another thing Suricata can observe is the traffic flow behavior. It sees the
   packet sizes, timing, and volume. Based on this information, if a sensor streams an abnormal amount of encrypted data, it
   could be a sign of data exfiltration. Additionally, if a massive flood of connection attempts to port 8883 is observed
   even if they fail the handshake, this can be detected as a DDoS attack.
