from tool_shed.base.twilltestcase import ShedTwillTestCase, common, os
import tool_shed.base.test_db_util as test_db_util

emboss_datatypes_repository_name = 'emboss_datatypes_0090'
emboss_datatypes_repository_description = "Datatypes for emboss"
emboss_datatypes_repository_long_description = "Long description of Emboss' datatypes"

emboss_repository_name = 'emboss_0090'
emboss_repository_description = "Galaxy's emboss tool"
emboss_repository_long_description = "Long description of Galaxy's emboss tool"

filtering_repository_name = 'filtering_0090'
filtering_repository_description = "Galaxy's filtering tool"
filtering_repository_long_description = "Long description of Galaxy's filtering tool"

freebayes_repository_name = 'freebayes_0090'
freebayes_repository_description = "Galaxy's freebayes tool"
freebayes_repository_long_description = "Long description of Galaxy's freebayes tool"

bwa_base_repository_name = 'bwa_base_0090'
bwa_base_repository_description = "BWA Base"
bwa_base_repository_long_description = "NT space mapping with BWA"

bwa_color_repository_name = 'bwa_color_0090'
bwa_color_repository_description = "BWA Color"
bwa_color_repository_long_description = "Color space mapping with BWA"

category_name = 'Test 0090 Tool Search And Installation'
category_description = 'Test 0090 Tool Search And Installation'

class TestRepositoryCircularDependenciesAgain( ShedTwillTestCase ):
    '''Test more features related to repository dependencies.'''
    def test_0000_initiate_users( self ):
        """Create necessary user accounts."""
        self.logout()
        self.login( email=common.test_user_1_email, username=common.test_user_1_name )
        test_user_1 = test_db_util.get_user( common.test_user_1_email )
        assert test_user_1 is not None, 'Problem retrieving user with email %s from the database' % test_user_1_email
        test_user_1_private_role = test_db_util.get_private_role( test_user_1 )
        self.logout()
        self.login( email=common.admin_email, username=common.admin_username )
        admin_user = test_db_util.get_user( common.admin_email )
        assert admin_user is not None, 'Problem retrieving user with email %s from the database' % admin_email
        admin_user_private_role = test_db_util.get_private_role( admin_user )
    def test_0005_create_bwa_base_repository( self ):
        '''Create and populate bwa_base_0090.'''
        category = self.create_category( name=category_name, description=category_description )
        self.logout()
        self.login( email=common.test_user_1_email, username=common.test_user_1_name )
        repository = self.get_or_create_repository( name=bwa_base_repository_name, 
                                                    description=bwa_base_repository_description, 
                                                    long_description=bwa_base_repository_long_description, 
                                                    owner=common.test_user_1_name,
                                                    category_id=self.security.encode_id( category.id ), 
                                                    strings_displayed=[] )
        self.upload_file( repository, 
                          filename='bwa/bwa_base.tar',
                          filepath=None,
                          valid_tools_only=True,
                          uncompress_file=True,
                          remove_repo_files_not_in_tar=False, 
                          commit_message='Uploaded BWA tarball.',
                          strings_displayed=[], 
                          strings_not_displayed=[] )
    def test_0010_create_bwa_color_repository( self ):
        '''Create and populate bwa_color_0090.'''
        category = self.create_category( name=category_name, description=category_description )
        self.logout()
        self.login( email=common.test_user_1_email, username=common.test_user_1_name )
        repository = self.get_or_create_repository( name=bwa_color_repository_name, 
                                                    description=bwa_color_repository_description, 
                                                    long_description=bwa_color_repository_long_description, 
                                                    owner=common.test_user_1_name,
                                                    category_id=self.security.encode_id( category.id ), 
                                                    strings_displayed=[] )
        self.upload_file( repository, 
                          filename='bwa/bwa_color.tar',
                          filepath=None,
                          valid_tools_only=True,
                          uncompress_file=True,
                          remove_repo_files_not_in_tar=False, 
                          commit_message='Uploaded BWA color tarball.',
                          strings_displayed=[], 
                          strings_not_displayed=[] )
    def test_0015_create_emboss_datatypes_repository( self ):
        '''Create and populate emboss_datatypes_0090.'''
        category = self.create_category( name=category_name, description=category_description )
        self.logout()
        self.login( email=common.test_user_1_email, username=common.test_user_1_name )
        repository = self.get_or_create_repository( name=emboss_datatypes_repository_name, 
                                                    description=emboss_datatypes_repository_description, 
                                                    long_description=emboss_datatypes_repository_long_description, 
                                                    owner=common.test_user_1_name,
                                                    category_id=self.security.encode_id( category.id ), 
                                                    strings_displayed=[] )
        self.upload_file( repository, 
                          filename='emboss/datatypes/datatypes_conf.xml',
                          filepath=None,
                          valid_tools_only=True,
                          uncompress_file=False,
                          remove_repo_files_not_in_tar=False, 
                          commit_message='Uploaded datatypes_conf.xml.',
                          strings_displayed=[], 
                          strings_not_displayed=[] )
    def test_0020_create_emboss_repository( self ):
        '''Create and populate emboss_0090.'''
        category = self.create_category( name=category_name, description=category_description )
        repository = self.get_or_create_repository( name=emboss_repository_name, 
                                                    description=emboss_repository_description, 
                                                    long_description=emboss_repository_long_description, 
                                                    owner=common.test_user_1_name,
                                                    category_id=self.security.encode_id( category.id ), 
                                                    strings_displayed=[] )
        self.upload_file( repository, 
                          filename='emboss/emboss.tar',
                          filepath=None,
                          valid_tools_only=True,
                          uncompress_file=False,
                          remove_repo_files_not_in_tar=False, 
                          commit_message='Uploaded emboss tarball.',
                          strings_displayed=[], 
                          strings_not_displayed=[] )
        datatypes_repository = test_db_util.get_repository_by_name_and_owner( emboss_datatypes_repository_name, common.test_user_1_name )
        repository_dependencies_path = self.generate_temp_path( 'test_0090', additional_paths=[ 'emboss' ] )
        self.generate_repository_dependency_xml( [ datatypes_repository ], 
                                                 self.get_filename( 'repository_dependencies.xml', filepath=repository_dependencies_path ), 
                                                 dependency_description='Emboss depends on the emboss_datatypes repository.' )
        self.upload_file( repository, 
                          filename='repository_dependencies.xml', 
                          filepath=repository_dependencies_path,
                          valid_tools_only=True,
                          uncompress_file=True,
                          remove_repo_files_not_in_tar=False, 
                          commit_message='Uploaded dependency on emboss_datatypes.',
                          strings_displayed=[], 
                          strings_not_displayed=[] )
    def test_0025_create_filtering_repository( self ):
        '''Create and populate filtering_0090.'''
        category = self.create_category( name=category_name, description=category_description )
        filtering_repository = self.get_or_create_repository( name=filtering_repository_name, 
                                                              description=filtering_repository_description, 
                                                              long_description=filtering_repository_long_description, 
                                                              owner=common.test_user_1_name,
                                                              category_id=self.security.encode_id( category.id ), 
                                                              strings_displayed=[] )
        self.upload_file( filtering_repository, 
                          filename='filtering/filtering_1.1.0.tar',
                          filepath=None,
                          valid_tools_only=True,
                          uncompress_file=True,
                          remove_repo_files_not_in_tar=False, 
                          commit_message='Uploaded filtering 1.1.0 tarball.',
                          strings_displayed=[], 
                          strings_not_displayed=[] )
        emboss_repository = test_db_util.get_repository_by_name_and_owner( emboss_repository_name, common.test_user_1_name )
        repository_dependencies_path = self.generate_temp_path( 'test_0090', additional_paths=[ 'filtering' ] )
        self.generate_repository_dependency_xml( [ emboss_repository ], 
                                                 self.get_filename( 'repository_dependencies.xml', filepath=repository_dependencies_path ), 
                                                 dependency_description='Filtering depends on the emboss repository.' )
        self.upload_file( filtering_repository, 
                          filename='repository_dependencies.xml', 
                          filepath=repository_dependencies_path,
                          valid_tools_only=True,
                          uncompress_file=False,
                          remove_repo_files_not_in_tar=False, 
                          commit_message='Uploaded dependency on emboss.',
                          strings_displayed=[], 
                          strings_not_displayed=[] )
    def test_0030_create_freebayes_repository( self ):
        '''Create and populate freebayes_0090.'''
        category = self.create_category( name=category_name, description=category_description )
        repository = self.get_or_create_repository( name=freebayes_repository_name, 
                                                    description=freebayes_repository_description, 
                                                    long_description=freebayes_repository_long_description, 
                                                    owner=common.test_user_1_name,
                                                    category_id=self.security.encode_id( category.id ), 
                                                    strings_displayed=[] )
        self.upload_file( repository, 
                          filename='freebayes/freebayes.tar',
                          filepath=None,
                          valid_tools_only=True,
                          uncompress_file=True,
                          remove_repo_files_not_in_tar=False, 
                          commit_message='Uploaded freebayes tarball.',
                          strings_displayed=[], 
                          strings_not_displayed=[] )
    def test_0035_create_and_upload_dependency_definitions( self ):
        '''Create and upload repository dependency definitions.'''
        bwa_color_repository = test_db_util.get_repository_by_name_and_owner( bwa_color_repository_name, common.test_user_1_name )
        bwa_base_repository = test_db_util.get_repository_by_name_and_owner( bwa_base_repository_name, common.test_user_1_name )
        emboss_datatypes_repository = test_db_util.get_repository_by_name_and_owner( emboss_datatypes_repository_name, common.test_user_1_name )
        emboss_repository = test_db_util.get_repository_by_name_and_owner( emboss_repository_name, common.test_user_1_name )
        filtering_repository = test_db_util.get_repository_by_name_and_owner( filtering_repository_name, common.test_user_1_name )
        freebayes_repository = test_db_util.get_repository_by_name_and_owner( freebayes_repository_name, common.test_user_1_name )
        dependency_xml_path = self.generate_temp_path( 'test_0090', additional_paths=[ 'freebayes' ] )
        self.create_repository_dependency( emboss_repository, depends_on=[ emboss_datatypes_repository ], filepath=dependency_xml_path )
        self.create_repository_dependency( filtering_repository, depends_on=[ freebayes_repository ], filepath=dependency_xml_path )
        self.create_repository_dependency( bwa_base_repository, depends_on=[ emboss_repository ], filepath=dependency_xml_path )
        self.create_repository_dependency( bwa_color_repository, depends_on=[ filtering_repository ], filepath=dependency_xml_path )
    def test_0040_verify_repository_dependencies( self ):
        '''Verify the generated dependency structure.'''
        bwa_color_repository = test_db_util.get_repository_by_name_and_owner( bwa_color_repository_name, common.test_user_1_name )
        bwa_base_repository = test_db_util.get_repository_by_name_and_owner( bwa_base_repository_name, common.test_user_1_name )
        emboss_datatypes_repository = test_db_util.get_repository_by_name_and_owner( emboss_datatypes_repository_name, common.test_user_1_name )
        emboss_repository = test_db_util.get_repository_by_name_and_owner( emboss_repository_name, common.test_user_1_name )
        filtering_repository = test_db_util.get_repository_by_name_and_owner( filtering_repository_name, common.test_user_1_name )
        freebayes_repository = test_db_util.get_repository_by_name_and_owner( freebayes_repository_name, common.test_user_1_name )
        self.check_repository_dependency( emboss_repository, emboss_datatypes_repository )
        self.check_repository_dependency( filtering_repository, freebayes_repository )
        self.check_repository_dependency( bwa_base_repository, emboss_repository )
        self.check_repository_dependency( bwa_color_repository, filtering_repository )