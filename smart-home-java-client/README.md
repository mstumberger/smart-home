Add this code to use client as router worker

        {
            "type": "guest",
            "executable": "java",
            "arguments": [
                "-classpath",
                "../smart-home-back-end/target/classes:../smart-home-back-end/target/dependency/*",
                "com.example.WampClient",
                "ws://127.0.0.1:8080/ws",
                "realm1"
            ],
            "options": {
                "workdir": ".."
            }
        }