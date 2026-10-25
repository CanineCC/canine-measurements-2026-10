using System.Text.Json;
using CodeHealth.CodeModel.Sidecars;
using CodeHealth.Core.Complexity;
using CodeHealth.Toolchain.Tools;
using Microsoft.Extensions.Logging.Abstractions;

// usage: JavaProbe <source-root> <out.jsonl>
var root = Path.GetFullPath(args[0]);
var model = await JvmSidecar.TryBuildAsync(new ProcessToolRunner(NullLogger<ProcessToolRunner>.Instance), root, root,
    NullLogger.Instance, CancellationToken.None);
if (model is null) { Console.Error.WriteLine("Java code model failed to build"); return 2; }
var calc = new CyclomaticComplexityCalculator(NullLogger<CyclomaticComplexityCalculator>.Instance);
var methods = await calc.ComputeAsync([], model, true, CancellationToken.None);
using var w = new StreamWriter(args[1]);
foreach (var m in methods)
    w.WriteLine(JsonSerializer.Serialize(new { path = Path.GetRelativePath(root, Path.GetFullPath(Path.Combine(root, m.FilePath))), method = m.MethodName, identity = m.IdentityName, line = m.LineNumber, endLine = m.EndLine, cyclomatic = m.CyclomaticScore, cognitive = m.CognitiveScore }));
Console.Error.WriteLine($"{model.Projects.Count} projects, {methods.Count} methods");
return 0;
