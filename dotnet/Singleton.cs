using System;

namespace CarinaMarketplace
{
    public class WikiGit
    {
        private WikiGit()
        {

        }

        private static readonly Lazy<WikiGit> instance = new Lazy<WikiGit>(() => new WikiGit());

        public static WikiGit Instance { get { return instance.Value; } }

    }
}
