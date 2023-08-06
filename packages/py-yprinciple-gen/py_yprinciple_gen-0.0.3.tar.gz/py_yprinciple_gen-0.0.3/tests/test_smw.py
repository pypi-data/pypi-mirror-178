'''
Created on 2022-11-24

@author: wf
'''
from collections import Counter
from meta.mw import SMWAccess
from meta.metamodel import Context
from tests.basemwtest import BaseMediawikiTest
from yprinciple.smw_targets import SMWTarget
from yprinciple.ypcell import YpCell
from wikibot.wikipush import WikiPush
from yprinciple.editor import Editor

class TestSMW(BaseMediawikiTest):
    """
    test Semantic MediaWiki handling
    """
    
    def setUp(self, debug=False, profile=True):
        BaseMediawikiTest.setUp(self, debug=debug, profile=profile)
        for wikiId in ["wiki","ceur-ws","cr"]:
            self.getWikiUser(wikiId, save=True)
            
    def test_ypCell(self):
        """
        test ypCell
        """
        debug=True
        smwAccess=SMWAccess("ceur-ws",debug=debug)
        counter=Counter()
        for mw_context in smwAccess.getMwContexts().values():
            context,error=Context.fromWikiContext(mw_context, debug=debug)
            self.assertIsNone(error)
            for target in SMWTarget.getSMWTargets().values():
                for topic in context.topics.values():
                    ypCell=YpCell(topic=topic,target=target)
                    ypCell.getPage(smwAccess)
                    counter[ypCell.status]+=1
                    if debug:
                        print(f"{ypCell.getLabelText()}:{ypCell.statusMsg}")
                        print(ypCell.pageUrl)
        if debug:
            print(counter.most_common())
        self.assertTrue(counter["✅"]>=92)
        
    def testGenerate(self):
        """
        test the generate functionality
        """
        debug=self.debug
        debug=True
        smwAccess=SMWAccess("cr",debug=debug)
        mw_contexts=smwAccess.getMwContexts()
        mw_context=mw_contexts["CrSchema"]
        context,error=Context.fromWikiContext(mw_context, debug=debug)
        self.assertIsNone(error)
        topic=context.topics["City"]
        withEditor=not self.inPublicCI()
        withEditor=False
        for target_key in ["category","concept","help","listOf"]:
            smwTarget=SMWTarget.getSMWTargets()[target_key]
            ypCell=YpCell(topic=topic,target=smwTarget,debug=debug)
            ypCell.generate(smwAccess=smwAccess,dryRun=True,withEditor=withEditor)