package com.example.order;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.*;

import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.Statement;
import java.sql.ResultSet;
import java.util.*;

@SpringBootApplication
@RestController
public class OrderApplication {

    private final DataSource dataSource;

    public OrderApplication(DataSource dataSource) {
        this.dataSource = dataSource;
    }

    public static void main(String[] args) {
        SpringApplication.run(OrderApplication.class, args);
    }

    @GetMapping("/")
    public Map<String, String> home() {

        Map<String, String> response = new HashMap<>();

        response.put("service", "Order Service");
        response.put("status", "running");

        return response;
    }

    @GetMapping("/health")
    public Map<String, String> health() {

        Map<String, String> response = new HashMap<>();

        response.put("service", "order-service");
        response.put("status", "UP");

        return response;
    }

    @GetMapping("/orders")
    public List<Map<String, Object>> orders() throws Exception {

        List<Map<String, Object>> orders = new ArrayList<>();

        try (Connection connection = dataSource.getConnection();
             Statement statement = connection.createStatement()) {

            ResultSet resultSet =
                    statement.executeQuery(
                            "SELECT id, product, quantity, status FROM orders"
                    );

            while (resultSet.next()) {

                Map<String, Object> order = new HashMap<>();

                order.put("id", resultSet.getInt("id"));
                order.put("product", resultSet.getString("product"));
                order.put("quantity", resultSet.getInt("quantity"));
                order.put("status", resultSet.getString("status"));

                orders.add(order);
            }
        }

        return orders;
    }
}