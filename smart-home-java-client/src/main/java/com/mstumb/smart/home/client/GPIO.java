package com.mstumb.smart.home.client;

import com.pi4j.Pi4J;
import com.pi4j.io.gpio.digital.DigitalInput;
import com.pi4j.io.gpio.digital.DigitalState;

import java.util.Properties;
import java.util.concurrent.TimeUnit;

/*
https://forums.raspberrypi.com/viewtopic.php?t=35006

https://github.com/zicowarn/DallasTempSensorDS18
*/


public class GPIO {
    public static void main(String[] args) {
        int DIGITAL_OUTPUT_PIN = 1;
        int DIGITAL_INPUT_PIN = 2;

        // Initialize Pi4J with an auto context
        // An auto context includes AUTO-DETECT BINDINGS enabled
        // which will load all detected Pi4J extension libraries
        // (Platforms and Providers) in the class path
        var pi4j = Pi4J.newAutoContext();

        // create a digital output instance using the default digital output provider
        var output = pi4j.dout().create(DIGITAL_OUTPUT_PIN);
        output.config().shutdownState(DigitalState.HIGH);

        // setup a digital output listener to listen for any state changes on the digital output
        output.addListener(System.out::println);

        // lets invoke some changes on the digital output
        output.state(DigitalState.HIGH)
                .state(DigitalState.LOW)
                .state(DigitalState.HIGH)
                .state(DigitalState.LOW);

        // lets toggle the digital output state a few times
        output.toggle()
                .toggle()
                .toggle();

        // another friendly method of setting output state
        output.high()
                .low();

        // lets read the digital output state
        System.out.print("CURRENT DIGITAL OUTPUT [" + output + "] STATE IS [");
        System.out.println(output.state() + "]");

        // pulse to HIGH state for 3 seconds
        System.out.println("PULSING OUTPUT STATE TO HIGH FOR 3 SECONDS");
        output.pulse(3, TimeUnit.SECONDS, DigitalState.HIGH);
        System.out.println("PULSING OUTPUT STATE COMPLETE");

        // shutdown Pi4J
        pi4j.shutdown();


        Properties properties = new Properties();
        properties.put("id", "my_digital_input");
        properties.put("address", DIGITAL_INPUT_PIN);
        properties.put("pull", "UP");
        properties.put("name", "MY-DIGITAL-INPUT");

        var config = DigitalInput.newConfigBuilder(pi4j)
                .load(properties)
                .build();

        var input = pi4j.din().create(config);

        input.addListener(e -> {
            if (e.state() == DigitalState.HIGH) {
                System.out.println("Button is pressed");
            }
        });

    }
}
