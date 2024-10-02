var builder = WebApplication.CreateBuilder(args);
_ = builder.Logging.SetMinimumLevel(LogLevel.Trace);
var app = builder.Build();

app.MapGet("/", () => "Hello World!");

app.Run();
