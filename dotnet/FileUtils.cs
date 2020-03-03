using Microsoft.CSharp;
using System;
using System.CodeDom.Compiler;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Utils
{
    public class FileUtils
    {
        public static void CompileCode(string codeAsString, string assembly, List<string> referencedAssemblies)
        {
            string dir = Path.GetDirectoryName(assembly);
            if (!Directory.Exists(dir))
            {
                Directory.CreateDirectory(dir);
            }
            CSharpCodeProvider codeProvider = new CSharpCodeProvider();
            var options = new CompilerParameters
            {
                GenerateExecutable = false,
                OutputAssembly = assembly
            };
            options.ReferencedAssemblies.AddRange(referencedAssemblies.ToArray());
            var compileRes = codeProvider.CompileAssemblyFromSource(options, new[] { codeAsString });
            if (compileRes.Errors.HasErrors)
            {
                var err = "";
                for (int i = 0; i < compileRes.Errors.Count; i++)
                {

                    err += $"{compileRes.Errors[i].FileName}({compileRes.Errors[i].Line}): error {compileRes.Errors[i].ErrorNumber}: {compileRes.Errors[i].ErrorText}";
                    err += System.Environment.NewLine;
                }
                throw new Exception(err);
            }
        }

        public static void Copy(string sourceDirectory, string targetDirectory)
        {
            DirectoryInfo diSource = new DirectoryInfo(sourceDirectory);
            DirectoryInfo diTarget = new DirectoryInfo(targetDirectory);

            CopyAll(diSource, diTarget);
        }

        public static void CopyAll(DirectoryInfo source, DirectoryInfo target)
        {
            Directory.CreateDirectory(target.FullName);

            // Copy each file into the new directory.
            foreach (FileInfo fi in source.GetFiles())
            {
                string dstFile = Path.Combine(target.FullName, fi.Name);
                fi.CopyTo(dstFile, true);
                File.SetAttributes(dstFile, FileAttributes.Normal);
            }

            // Copy each subdirectory using recursion.
            foreach (DirectoryInfo diSourceSubDir in source.GetDirectories())
            {
                DirectoryInfo nextTargetSubDir =
                    target.CreateSubdirectory(diSourceSubDir.Name);
                CopyAll(diSourceSubDir, nextTargetSubDir);
            }
        }

        public static IEnumerable<string> EnumerateFiles(string root, string relativePath = "")
        {
            string dir = Path.Combine(root, relativePath);
            if (!Directory.Exists(dir))
            {
                throw new Exception(string.Format("\"{0}\" is not a directory.", dir));
            }

            var directoryInfo = new DirectoryInfo(dir);
            foreach (var item in directoryInfo.GetFiles())
            {
                if (item.Name.StartsWith(".git")) { continue; }
                yield return Path.Combine(relativePath, item.Name);
            }
            foreach (var item in directoryInfo.GetDirectories())
            {
                // skip .git folder
                if (item.Name.ToLower() == ".git") { continue; }
                string newRelativePath = Path.Combine(relativePath, item.Name);
                foreach (var file in EnumerateFiles(root, newRelativePath))
                {
                    yield return file;
                }
            }
        }
    }
}
