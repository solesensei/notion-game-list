import typing as tp


class SteamStoreAppPriceOverview:

    def __init__(
        self,
        currency: str,
        initial: int,
        final: int,
        discount_percent: int,
        initial_formatted: str,
        final_formatted: str,
    ):
        self.currency = currency
        self.initial = initial
        self.final = final
        self.discount_percent = discount_percent
        self.initial_formatted = initial_formatted
        self.final_formatted = final_formatted


class SteamStoreAppPackageGroupSub:

    def __init__(
        self,
        packageid: int,
        percent_savings_text: str,
        percent_savings: int,
        option_text: str,
        option_description: str,
        can_get_free_license: str,
        is_free_license: bool,
        price_in_cents_with_discount: int
    ):
        self.packageid = packageid
        self.percent_savings_text = percent_savings_text
        self.percent_savings = percent_savings
        self.option_text = option_text
        self.option_description = option_description
        self.can_get_free_license = can_get_free_license
        self.is_free_license = is_free_license
        self.price_in_cents_with_discount = price_in_cents_with_discount


class SteamStoreAppPackageGroup:

    def __init__(
        self,
        name: str,
        title: str,
        description: str,
        selection_text: str,
        save_text: str,
        display_type: int,
        is_recurring_subscription: str,
        subs: tp.List[SteamStoreAppPackageGroupSub]
    ):
        self.name = name
        self.title = title
        self.description = description
        self.selection_text = selection_text
        self.save_text = save_text
        self.display_type = display_type
        self.is_recurring_subscription = is_recurring_subscription
        self.subs = subs


class SteamStoreAppCategory:

    def __init__(self, id: int, description: str):
        self.id = id
        self.description = description


class SteamStoreAppGenre:

    def __init__(self, id: str, description: str):
        self.id = id
        self.description = description


class SteamStoreAppScreenshot:

    def __init__(self, id: int, path_thumbnail: str, path_full: str):
        self.id = id
        self.path_thumbnail = path_thumbnail
        self.path_full = path_full


class SteamStoreAppMovie:

    def __init__(
        self,
        id: int,
        name: str,
        thumbnail: str,
        webm: tp.Dict[str, str],
        mp4: tp.Dict[str, str],
        highlight: bool
    ):
        self.id = id
        self.name = name
        self.thumbnail = thumbnail
        self.webm = webm
        self.mp4 = mp4
        self.highlight = highlight


class SteamStoreAppMetacriticScore:

    def __init__(self, score: int, url: str):
        self.score = score
        self.url = url


class SteamStoreAppAchievementHighlighted:

    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path


class SteamStoreAppAchievements:

    def __init__(self, total: int, highlighted: tp.List[SteamStoreAppAchievementHighlighted]):
        self.total = total
        self.highlighted = highlighted


class SteamStoreAppReleaseDate:

    def __init__(self, coming_soon: bool, date: str):
        self.coming_soon = coming_soon
        self.date = date


class SteamStoreAppSupportInfo:

    def __init__(self, url: str, email: str):
        self.url = url
        self.email = email


class SteamStoreAppContentDescriptors:

    def __init__(self, ids: tp.List[int], notes: str):
        self.ids = ids
        self.notes = notes


class SteamStoreApp:

    def __init__(
        self,
        type: str,
        name: str,
        steam_appid: int,
        required_age: tp.Union[str, int],
        is_free: bool,
        detailed_description: str,
        about_the_game: str,
        short_description: str,
        supported_languages: str,
        header_image: str,
        developers: tp.List[str],
        publishers: tp.List[str],
        packages: tp.List[int],
        platforms: tp.Dict[str, bool],
        metacritic: SteamStoreAppMetacriticScore,
        categories: tp.List[SteamStoreAppCategory],
        genres: tp.List[SteamStoreAppGenre],
        screenshots: tp.List[SteamStoreAppScreenshot],
        movies: tp.List[SteamStoreAppMovie],
        recommendations: tp.Dict[str, int],
        achievements: SteamStoreAppAchievements,
        release_date: SteamStoreAppReleaseDate,
        support_info: SteamStoreAppSupportInfo,
        package_groups: tp.List[SteamStoreAppPackageGroup],
        background: str,
        content_descriptors: SteamStoreAppContentDescriptors,
        price_overview: tp.Optional[SteamStoreAppPriceOverview] = None,
        reviews: tp.Optional[str] = None,
        legal_notice: tp.Optional[str] = None,
        demos: tp.Optional[tp.List[dict]] = None,
        dlc: tp.Optional[tp.List[int]] = None,
        website: tp.Optional[str] = None,
        pc_requirements: tp.Dict[str, str] = None,
        mac_requirements: tp.Dict[str, str] = None,
        linux_requirements: tp.Dict[str, str] = None,
        **kwargs,
    ):
        self.type = type
        self.name = name
        self.steam_appid = steam_appid
        self.required_age = required_age
        self.is_free = is_free
        self.detailed_description = detailed_description
        self.about_the_game = about_the_game
        self.short_description = short_description
        self.supported_languages = supported_languages
        self.header_image = header_image
        self.developers = developers
        self.publishers = publishers
        self.packages = packages
        self.platforms = platforms
        self.metacritic = metacritic
        self.categories = categories
        self.genres = genres
        self.screenshots = screenshots
        self.movies = movies
        self.recommendations = recommendations
        self.achievements = achievements
        self.release_date = release_date
        self.support_info = support_info
        self.package_groups = package_groups
        self.background = background
        self.content_descriptors = content_descriptors
        self.price_overview = price_overview
        self.reviews = reviews
        self.legal_notice = legal_notice
        self.demos = demos
        self.dlc = dlc
        self.website = website
        self.pc_requirements = pc_requirements
        self.mac_requirements = mac_requirements
        self.linux_requirements = linux_requirements
