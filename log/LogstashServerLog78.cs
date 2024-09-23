using System;
using System.Net.Http;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace www778878net.log
{
    /// <summary>
    /// Logstash server logger
    /// *Note: If errorLevel is greater than or equal to Log78's LevelApi, it may cause an infinite loop when sending logs to Logstash fails
    /// </summary>
    public class LogstashServerLog78 : IServerLog78, IDisposable
    {
        public string ServerUrl { get; set; }
        // 添加新属性
        public bool ThrowOnError { get; set; } = false;
        private readonly HttpClient _httpClient;
        private readonly Log78 _logger;
        private readonly SemaphoreSlim _semaphore = new SemaphoreSlim(10); // 限制最大并发请求数为10

        /// <summary>
        /// 
        /// </summary>
        /// <param name="serverUrl"></param>
        /// <param name="errorLevel">Must be less than Log78's LevelApi to avoid potential infinite loops</param>
        /// <exception cref="ArgumentOutOfRangeException">Thrown when errorLevel is greater than or equal to Log78's LevelApi</exception>
        public LogstashServerLog78(string serverUrl, int levelFile = 50)
        {
            ServerUrl = serverUrl;
            
            _httpClient = new HttpClient();
            _httpClient.Timeout = TimeSpan.FromSeconds(30); // 设置30秒超时
            _logger = new Log78();
            _logger.SetupLevel(levelFile, levelFile, 99999);
        }

        public async Task<HttpResponseMessage?> LogToServer(LogEntry logEntry)
        {
            await _semaphore.WaitAsync();
            try
            {
                using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(30));

                try
                {
                    return await LogToServerInternal(logEntry, cts.Token).ConfigureAwait(false);
                }
                catch (OperationCanceledException)
                {
                    await _logger.ERROR(new LogEntry { Basic = new BasicInfo { Message = "LogToServer operation timed out", Summary = "Logstash Timeout" } }).ConfigureAwait(false);
                    return null;
                }
                catch (Exception ex)
                {
                    await _logger.ERROR(new LogEntry { Basic = new BasicInfo { Message = $"Unexpected error in LogToServer: {ex.Message}", Summary = "Logstash Error" } }).ConfigureAwait(false);
                    return null;
                }
            }
            finally
            {
                _semaphore.Release();
            }
        }

        private async Task<HttpResponseMessage?> LogToServerInternal(LogEntry logEntry, CancellationToken cancellationToken)
        {
            try
            {
                string jsonContent = logEntry.ToJson();
                var content = new StringContent(jsonContent, Encoding.UTF8, "application/json");

                using var timeoutCts = new CancellationTokenSource(TimeSpan.FromSeconds(20));
                using var linkedCts = CancellationTokenSource.CreateLinkedTokenSource(cancellationToken, timeoutCts.Token);

                var response = await _httpClient.PostAsync(ServerUrl, content, linkedCts.Token).ConfigureAwait(false);

                if (response.IsSuccessStatusCode)
                {
                    await _logger.DEBUG(new LogEntry { Basic = new BasicInfo { Message = "Logstash log sent successfully", Summary = "Logstash Success" } }).ConfigureAwait(false);
                }
                else
                {
                    var errorMessage = $"Failed to send log to Logstash. Status code: {response.StatusCode}";
                    await _logger.ERROR(new LogEntry { Basic = new BasicInfo { Message = errorMessage, Summary = "Logstash Error" } }).ConfigureAwait(false);
                    if (ThrowOnError)
                    {
                        throw new HttpRequestException(errorMessage);
                    }
                }
                return response;
            }
            catch (OperationCanceledException)
            {
                await _logger.ERROR(new LogEntry { Basic = new BasicInfo { Message = "HTTP request was canceled or timed out", Summary = "Logstash Canceled" } }).ConfigureAwait(false);
                return null;
            }
            catch (Exception ex)
            {
                var errorMessage = $"Error sending log to Logstash: {ex.Message}";
                await _logger.ERROR(new LogEntry { Basic = new BasicInfo { Message = errorMessage, Summary = "Logstash Exception" } }).ConfigureAwait(false);
                if (ThrowOnError)
                {
                    throw;
                }
                return null;
            }
        }

        public void Dispose()
        {
            _httpClient?.Dispose();
        }
    }
}