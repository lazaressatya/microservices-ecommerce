using Npgsql;

var builder = WebApplication.CreateBuilder(args);

var app = builder.Build();

var connectionString =
    Environment.GetEnvironmentVariable("POSTGRES_CONNECTION")
    ?? "Host=payment-postgres;Port=5432;Database=paymentsdb;Username=postgres;Password=postgres";

app.MapGet("/", () =>
{
    return Results.Ok(new
    {
        service = "Payment Service",
        status = "running"
    });
});

app.MapGet("/health", () =>
{
    return Results.Ok(new
    {
        service = "payment-service",
        status = "UP"
    });
});

app.MapGet("/payments", async () =>
{
    var payments = new List<object>();

    await using var connection =
        new NpgsqlConnection(connectionString);

    await connection.OpenAsync();

    await using var command =
        new NpgsqlCommand(
            "SELECT id, order_id, amount, status FROM payments",
            connection);

    await using var reader =
        await command.ExecuteReaderAsync();

    while (await reader.ReadAsync())
    {
        payments.Add(new
        {
            id = reader.GetInt32(0),
            orderId = reader.GetInt32(1),
            amount = reader.GetDecimal(2),
            status = reader.GetString(3)
        });
    }

    return Results.Ok(payments);
});

app.Run();