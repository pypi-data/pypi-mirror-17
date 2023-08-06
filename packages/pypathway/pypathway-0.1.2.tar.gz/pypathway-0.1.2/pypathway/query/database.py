from ..query.common import KEGGPathwayData, SupportedDatabase, CommonPathwayData, WiKiPathwayData, KEGGPathwayDataList
from ..query.network import NetworkRequest, NetworkMethod, NetworkException
import json
from Queue import Queue


class SearchResult:
    def __init__(self, comment, providers, numhits, results, empty):
        self.comment = comment
        self.providers = providers
        self.numhits = numhits
        self.results = results
        self.empty = empty

    '''
    This class store the total results of a public pathway database (Pathway Common, KEGG will not return this) search,
     this class should only used for the return value of PublicDatabase.search(), should not init singly

    Attributes:
        comment: the comment of a pathway search from Pathway Common
        providers: the total source of the providers
        numhits: the total results
        results: the lists of the result objects
        empty: if returns a empty rearch result
    '''

    def visualize(self):
        '''
        This function provide a quick view of the search result, it provide the the summary and the quick view of
        the pathway map

        Notes: Please do not call this method without ipython notebook, it will pop up a series of matplotlib
        plot windows.

        We recommend you do search operation in a ipython notebook, while get proper pathway file, the write the
         data integrating applications
        '''
        raise NotImplementedError()
        pass

    def __repr__(self):
        return "Get {} result\n{}".format(self.numhits, str(self.results))


class PublicDatabase:
    '''
    This class Provide the methods for pathway search, including KEGG and PathwayCommon.

    Args:
        database: member in common.SupportedDatabase, if you want to search all database, using SupportedDatabase.ALL

    Attributes:
        name: database

    Methods:
        kegg_search: search KEGG using KEGG's rest api
        common_search: search other database using Pathway Common's api
    '''
    def __init__(self, database=None):
        self.name = database

    def search(self, keyword):
        pass

    # directly retrieve, if not found, raise PathwayNotExistException
    # if database = ALL and no args here, will raise DatabaseNotSpecificException
    def retrieve(self, id, database=None):
        pass

    @staticmethod
    def search_wp(keyword, species=None, proxies=None):
        '''
        Search WikiPathway database using WikiPathway's rest api
        note if you want more function use webservice.
        :param keyword: The search keyword
        :param species: The target species
        :param proxies: proxies used by while requesting data.
        :return: a list of search result
        '''
        if species:
            url = "http://webservice.wikipathways.org/findPathwaysByText?query={}&species={}&format=json".format(
                keyword, species
            )
        else:
            url = "http://webservice.wikipathways.org/findPathwaysByText?query={}&format=json".format(
                keyword
            )
        res = NetworkRequest(url, NetworkMethod.GET, proxy=proxies)
        try:
            data = json.loads(res.text)
        except:
            raise Exception("Json parse exception")
        results = []
        for x in data["result"]:
            pw = WiKiPathwayData(x["id"], x["name"], x["species"], x["score"], x["revision"])
            pw.retrieve(proxies=proxies)
            results.append(pw)
        pool = [x.threads[0] for x in results]
        [x.join() for x in pool]
        return results

    @staticmethod
    def search_kegg(keyword, organism="hsa", proxies=None):
        '''
        Search KEGG database using KEGG's rest api.
        :param keyword: The search keyword
        :param organism: the organism
        :param proxies: proxies used by while requesting data.
        :return: a list of search result(instance of KEGGPathwayData)
        '''
        url = "http://rest.kegg.jp/find/pathway/{}".format(keyword)
        try:
            res = NetworkRequest(url, NetworkMethod.GET, proxy=proxies)
        except NetworkException as e:
            raise e
        if len(res.text) <= 1:
            return []
        else:
            # indicate that search in kegg contains data.
            results = [KEGGPathwayData(x.split("\t")[0][8:], x.split("\t")[1], organism)
                         for x in res.text.split("\n") if len(x) > 0]
            pathways = KEGGPathwayDataList(results=results)
            # fill the png and KGML data
            error = Queue()
            [p.retrieve(organism) for p in pathways]
            [p.join_active_thread() for p in pathways]
            if not error.empty():
                e = error.get()
                raise NetworkException(e[0], e[1])
            return pathways

    @staticmethod
    def search_reactome(keyword, organism=None, proxies=None):
        '''
        Search Reactome database
        :param keyword: The keyword using while searching.
        :param proxies: if not None, the proxies use while searching.
        :param organism: the target organism
        :return: a list of search result
        '''
        try:
            if organism:
                return PublicDatabase.common_search(keyword,
                                                    source=[SupportedDatabase.REACTOME],
                                                    organism=[organism],
                                                    proxies=proxies).results
            else:
                return PublicDatabase.common_search(keyword,
                                                    source=[SupportedDatabase.REACTOME],
                                                    proxies=proxies).results
        except Exception as e:
            raise e

    @staticmethod
    def _check_list_arg(arg):
        '''
        Private function, check if args is a list or None
        :param arg:
        :return:
        '''
        for x in arg:
            if x is not None and not isinstance(x, list):
                return False
        else:
            return True

    @staticmethod
    def common_search(q, source=None, organism=None, proxies=None):
        '''
        This method search the Pathway databases
        :param q: the keyword, more advance usage please visit pathway common
        :param source: a list of SupportedDatabase members, the pathway database search for.
        :param organism: currently support human.
        :param proxies: proxies used by while requesting data.
        :raise NetworkException if failed to build the connection to public database.
        :return: instance of SearchResult.
        '''
        # Check if the input is a list.
        if not PublicDatabase._check_list_arg([source, organism]):
            raise ValueError("argument should be a list")
        # Generating urls
        args = {
            k: v for (k, v) in {"q": [q], "datasource": source, "organism": organism, "type": type}.items() if v
        }
        args["type"] = ["pathway"]
        params = ["and".join(["{}={}".format(k, value) for value in v]) for k, v in args.items()]
        url = "http://www.pathwaycommons.org/pc2/search.json?" + "&".join(
            [p for p in params]
        )
        # perform a network request
        # print url
        try:
            nr = NetworkRequest(url, NetworkMethod.GET, proxy=proxies)
        except Exception as e:
            raise e
        if "Error 460" in nr.text:
            return SearchResult(None, None, 0, [], True)
        res_json = json.loads(nr.text)
        # Conclude the result.
        results = []
        for res in res_json.get("searchHit"):
            results.append(CommonPathwayData(res["uri"], res["name"], res["dataSource"], None, None, None))
        # jobs = []
        # for x in results:
        #     x.fill_data()
        #     jobs.extend(x.threads)
        # [j.start() for j in jobs]
        # [j.join() for j in jobs]
        return SearchResult(res_json.get("comment"), res_json.get("providers"), res_json.get("numHits"),
                            results, res_json.get("empty"))


if __name__ == '__main__':
    db = PublicDatabase()
    result = db.common_search("T cell", [SupportedDatabase.BioGRID, SupportedDatabase.REACTOME])
    print(result)