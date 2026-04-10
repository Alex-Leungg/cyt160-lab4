1. There was only 1 alert events for SID 2000001 in eve.json. The threshold keyword acts as a gatekeeper for your alerts. It doesn't 
   just check if a rule is "true"; it controls the frequency and volume of alerts written to eve.json to prevent your logs from being 
   overwhelmed by a single event.

2. On port 1883 data is sent as raw bytes over the network. Suricata acts like a passive listener, reading every MQTT control header 
   and JSON payload exactly as they appear. This allows your rules for "undefined" strings or buffer overflow patterns to match directly 
   against the packet contents. On port 8883, before the data leaves the Raspberry Pi, it is encrypted using a Transport Layer Security 
   (TLS) handshake. To an outside observer like Suricata, the payload looks like random, unreadable noise. Without the unique private key 
   held by the broker, Suricata cannot "unscramble" the encryption to see the actual MQTT messages or JSON data inside. 

   The trade-off between using plaintext (Port 1883) and TLS (Port 8883) for testing centers on visibility versus realism. In plaintext, 
   Suricata has full access to the packet payload, allowing you to verify that your content matching rules like detecting "undefined" 
   strings or buffer overflow patterns—actually work as intended. However, this is less realistic for modern systems. In contrast, 
   TLS provides a more secure, real-world environment, but it effectively "blinds" Suricata to the payload. While the rate-limit rule 
   would still trigger because it only needs to see the IP headers and port numbers, your malformed JSON rules would never fire because 
   the attack strings are scrambled by encryption.

3. No, the rule would not fire if the pattern started at byte 200 because byte 200 is beyond the depth. The depth: keyword tells Suricata 
   how far into the payload it should look for a match, starting from the very first byte. With depth:100, Suricata only scans the first 
   100 bytes of the packet's data. To detect a pattern that starts later in the packet you should increase the depth to ensure it covers 
   farther into the payload or remove the depth keyword entirely.


4. In the rule files you need to change the word 'alert' to 'drop' so the command is drop tcp any any... The drop keyword tells the engine 
   to discard the packet immediately and stop it from reaching the MQTT broker. In the Suricata/Docker configuration, you must modify 
   suricata.yaml to enable the nfqueue section. This tells Suricata to process packets from a specific queue. 
   Additionally, you must start Suricata with the -q flag followed by the queue number (e.g., -q 0) instead of the standard -i eth0.
